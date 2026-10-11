import logging

from rest_framework import viewsets, mixins, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated

from .models import ChatConversation
from .serializers import (
    ChatbotRequestSerializer,
    ChatConversationDetailSerializer,
    ChatConversationListSerializer,
)
from .agent import run_agent

logger = logging.getLogger(__name__)

TITLE_MAX_LENGTH = 60


class ChatbotViewSet(viewsets.GenericViewSet, mixins.CreateModelMixin):
    permission_classes = (AllowAny,)
    serializer_class = ChatbotRequestSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        question = serializer.validated_data["question"].strip()
        max_rows = serializer.validated_data.get("max_rows", 50)
        conversation_id = serializer.validated_data.get("conversation_id")

        try:
            result = run_agent(question, max_rows=max_rows)
        except RuntimeError as exc:
            return Response(
                {"success": False, "error": str(exc)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
        except Exception:
            logger.exception("Chatbot request failed unexpectedly (question=%r)", question)
            return Response(
                {"success": False, "error": "Chatbot failed to generate a response."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

        # Anonymous callers still get a normal answer; history is only kept
        # for logged-in users (there's no "their history" to attribute it to otherwise).
        if request.user and request.user.is_authenticated:
            conversation = self._get_or_create_conversation(request.user, conversation_id, question)
            conversation.messages.create(
                question=question,
                answer=result.get("answer", ""),
                sql=result.get("sql", ""),
                results=result.get("results"),
            )
            conversation.save(update_fields=["updated_at"])
            result["conversation_id"] = conversation.id

        return Response(result, status=status.HTTP_200_OK)

    @staticmethod
    def _get_or_create_conversation(user, conversation_id, question):
        if conversation_id:
            conversation = ChatConversation.objects.filter(pk=conversation_id, user=user).first()
            if conversation:
                return conversation

        title = question if len(question) <= TITLE_MAX_LENGTH else question[: TITLE_MAX_LENGTH - 1] + "…"
        return ChatConversation.objects.create(user=user, title=title)


class ChatConversationViewSet(
    viewsets.GenericViewSet, mixins.ListModelMixin, mixins.RetrieveModelMixin, mixins.DestroyModelMixin
):
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return ChatConversation.objects.filter(user=self.request.user)

    def get_serializer_class(self):
        if self.action == "list":
            return ChatConversationListSerializer
        return ChatConversationDetailSerializer

    def list(self, request, *args, **kwargs):
        serializer = self.get_serializer(self.get_queryset(), many=True)
        return Response({"success": True, "conversations": serializer.data})

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response({"success": True, "conversation": serializer.data})

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return Response({"success": True}, status=status.HTTP_200_OK)
