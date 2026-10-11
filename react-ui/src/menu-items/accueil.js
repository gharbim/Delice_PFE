// assets
import { IconHome } from '@tabler/icons';

//-----------------------|| ACCUEIL MENU ITEM ||-----------------------//

export const accueil = {
    id: 'accueil-group',
    type: 'group',
    children: [
        {
            id: 'accueil',
            title: 'Accueil',
            type: 'item',
            url: '/dashboard/accueil',
            icon: IconHome,
            breadcrumbs: false
        }
    ]
};
