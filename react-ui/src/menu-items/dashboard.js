// assets
import {
    IconDashboard,
    IconFileText,
    IconFileX,
    IconAlertTriangle,
    IconCreditCard,
    IconReceiptOff
} from '@tabler/icons';

// constant
const icons = {
    IconDashboard,
    IconFileText,
    IconFileX,
    IconAlertTriangle,
    IconCreditCard,
    IconReceiptOff
};

//-----------------------|| DASHBOARD MENU ITEMS ||-----------------------//

export const dashboard = {
    id: 'dashboard',
    title: 'Tableaux de bord Power BI',
    type: 'group',
    children: [
        {
            id: 'default',
            title: 'Production 1',
            description: 'Tableau de bord Production 1',
            type: 'item',
            url: '/dashboard/default',
            icon: icons['IconDashboard'],
            breadcrumbs: false
        },
        {
            id: 'emission',
            title: 'Production 2',
            description: 'Tableau de bord Production 2',
            type: 'item',
            url: '/dashboard/emission',
            icon: icons['IconFileText'],
            breadcrumbs: false
        },
        {
            id: 'annulation',
            title: 'Arrêts',
            description: 'Tableau de bord des arrêts de production',
            type: 'item',
            url: '/dashboard/annulation',
            icon: icons['IconFileX'],
            breadcrumbs: false
        }
    ]
};
