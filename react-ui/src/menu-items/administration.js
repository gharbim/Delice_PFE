// assets
import { IconUsers } from '@tabler/icons';

// constant
const icons = {
    IconUsers
};

//-----------------------|| ADMINISTRATION MENU ITEMS ||-----------------------//

export const administration = {
    id: 'administration',
    title: 'Administration',
    type: 'group',
    children: [
        {
            id: 'users',
            title: 'Utilisateurs',
            description: 'Gestion des comptes utilisateurs et des accès',
            type: 'item',
            url: '/admin/users',
            icon: icons['IconUsers'],
            breadcrumbs: false
        }
    ]
};
