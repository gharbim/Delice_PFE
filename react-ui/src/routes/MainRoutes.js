import React, { lazy } from 'react';
import { Route, Switch, useLocation } from 'react-router-dom';

// project imports
import MainLayout from './../layout/MainLayout';
import Loadable from '../ui-component/Loadable';
import AuthGuard from './../utils/route-guard/AuthGuard';

// dashboard routing
const AccueilView = Loadable(lazy(() => import('../views/Accueil')));
const DashboardDefault = Loadable(lazy(() => import('../views/dashboard/Default')));
const DashboardEmission = Loadable(lazy(() => import('../views/Emission')));
const DashboardAnnulation = Loadable(lazy(() => import('../views/Annulation')));
const DashboardImpaye = Loadable(lazy(() => import('../views/Impaye')));
const DashboardSinistre = Loadable(lazy(() => import('../views/Sinistre')));
const DashboardReglement = Loadable(lazy(() => import('../views/Reglement')));

// administration routing
const UserManagementView = Loadable(lazy(() => import('../views/UserManagement')));

// utilities routing
const UtilsTypography = Loadable(lazy(() => import('../views/utilities/Typography')));
const UtilsColor = Loadable(lazy(() => import('../views/utilities/Color')));
const UtilsShadow = Loadable(lazy(() => import('../views/utilities/Shadow')));
const UtilsMaterialIcons = Loadable(lazy(() => import('../views/utilities/MaterialIcons')));
const UtilsTablerIcons = Loadable(lazy(() => import('../views/utilities/TablerIcons')));

// sample page routing
const SamplePage = Loadable(lazy(() => import('../views/sample-page')));

//-----------------------|| MAIN ROUTING ||-----------------------//

const MainRoutes = () => {
    const location = useLocation();

    return (
        <Route
            path={[
                '/dashboard/accueil',
                '/dashboard/default',
                '/dashboard/emission',
                '/dashboard/annulation',
                '/dashboard/impaye',
                '/dashboard/sinistre',
                '/dashboard/reglement',
                '/utils/util-typography',
                '/utils/util-color',
                '/utils/util-shadow',
                '/icons/tabler-icons',
                '/icons/material-icons',
                '/admin/users',

                '/sample-page'
            ]}
        >
            <MainLayout>
                <Switch location={location} key={location.pathname}>
                    <AuthGuard>
                            <Route path="/dashboard/accueil" component={AccueilView} />
                            <Route path="/dashboard/default" component={DashboardDefault} />
                        <Route path="/dashboard/emission" component={DashboardEmission} />
                        <Route path="/dashboard/annulation" component={DashboardAnnulation} />
                        <Route path="/dashboard/impaye" component={DashboardImpaye} />
                        <Route path="/dashboard/sinistre" component={DashboardSinistre} />
                        <Route path="/dashboard/reglement" component={DashboardReglement} />
                        <Route path="/utils/util-typography" component={UtilsTypography} />
                        <Route path="/utils/util-color" component={UtilsColor} />
                        <Route path="/utils/util-shadow" component={UtilsShadow} />
                        <Route path="/icons/tabler-icons" component={UtilsTablerIcons} />
                        <Route path="/icons/material-icons" component={UtilsMaterialIcons} />
                        <Route path="/admin/users" component={UserManagementView} />

                        <Route path="/sample-page" component={SamplePage} />
                    </AuthGuard>
                </Switch>
            </MainLayout>
        </Route>
    );
};

export default MainRoutes;
