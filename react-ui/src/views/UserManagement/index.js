import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { useSelector } from 'react-redux';

// material-ui
import {
    Alert,
    Box,
    Button,
    Chip,
    CircularProgress,
    Table,
    TableBody,
    TableCell,
    TableContainer,
    TableHead,
    TableRow
} from '@material-ui/core';

// project imports
import MainCard from '../../ui-component/cards/MainCard';
import configData from '../../config';

const getErrorMessage = (error) => error?.response?.data?.msg || error?.message || "Une erreur s'est produite.";

const UserManagement = () => {
    const account = useSelector((state) => state.account);
    const [users, setUsers] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);
    const [savingId, setSavingId] = useState(null);
    const [feedback, setFeedback] = useState(null);

    const authHeaders = { headers: { Authorization: account.token } };

    useEffect(() => {
        axios
            .get(configData.API_SERVER + 'users/edit', authHeaders)
            .then((response) => setUsers(response.data.users || []))
            .catch((err) => setError(getErrorMessage(err)))
            .finally(() => setLoading(false));
        // eslint-disable-next-line react-hooks/exhaustive-deps
    }, []);

    const updateUser = (user, payload, successMessage) => {
        setSavingId(user.id);
        setFeedback(null);
        axios
            .patch(configData.API_SERVER + `users/edit/${user.id}`, payload, authHeaders)
            .then((response) => {
                setUsers((prev) => prev.map((u) => (u.id === user.id ? { ...u, ...response.data.user } : u)));
                setFeedback({ type: 'success', message: successMessage });
            })
            .catch((err) => setFeedback({ type: 'error', message: getErrorMessage(err) }))
            .finally(() => setSavingId(null));
    };

    const handleToggleActive = (user) =>
        updateUser(
            user,
            { is_active: !user.is_active },
            `${user.username} a été ${user.is_active ? 'désactivé' : 'réactivé'}.`
        );

    return (
        <MainCard title="Utilisateurs">
            {feedback && (
                <Alert severity={feedback.type} sx={{ mb: 2 }} onClose={() => setFeedback(null)}>
                    {feedback.message}
                </Alert>
            )}
            {error && (
                <Alert severity="error" sx={{ mb: 2 }}>
                    {error}
                </Alert>
            )}
            {loading ? (
                <Box sx={{ display: 'flex', justifyContent: 'center', py: 5 }}>
                    <CircularProgress />
                </Box>
            ) : (
                <TableContainer>
                    <Table>
                        <TableHead>
                            <TableRow>
                                <TableCell>Nom d'utilisateur</TableCell>
                                <TableCell>Email</TableCell>
                                <TableCell>Inscrit le</TableCell>
                                <TableCell>Statut</TableCell>
                                <TableCell align="right">Action</TableCell>
                            </TableRow>
                        </TableHead>
                        <TableBody>
                            {users.map((user) => {
                                const isSelf = user.id === account?.user?._id;
                                const isSaving = savingId === user.id;
                                return (
                                    <TableRow key={user.id} hover>
                                        <TableCell>{user.username}</TableCell>
                                        <TableCell>{user.email}</TableCell>
                                        <TableCell>{new Date(user.date).toLocaleDateString()}</TableCell>
                                        <TableCell>
                                            <Chip
                                                label={user.is_active ? 'Actif' : 'Désactivé'}
                                                color={user.is_active ? 'success' : 'default'}
                                                size="small"
                                            />
                                        </TableCell>
                                        <TableCell align="right">
                                            <Button
                                                size="small"
                                                color={user.is_active ? 'error' : 'primary'}
                                                disabled={isSelf || isSaving}
                                                onClick={() => handleToggleActive(user)}
                                                title={isSelf ? 'Vous ne pouvez pas désactiver votre propre compte' : undefined}
                                            >
                                                {user.is_active ? 'Désactiver' : 'Activer'}
                                            </Button>
                                        </TableCell>
                                    </TableRow>
                                );
                            })}
                        </TableBody>
                    </Table>
                </TableContainer>
            )}
        </MainCard>
    );
};

export default UserManagement;
