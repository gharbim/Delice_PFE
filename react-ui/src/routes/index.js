import React from 'react';
import { Switch } from 'react-router-dom';

// routes
import LandingRoute from './LandingRoute';
import MainRoutes from './MainRoutes';
import LoginRoutes from './LoginRoutes';
import AuthenticationRoutes from './AuthenticationRoutes';

//-----------------------|| ROUTING RENDER ||-----------------------//

const Routes = () => {
    return (
        <Switch>
            <React.Fragment>
                {/* Public landing page at / */}
                <LandingRoute />

                {/* Routes for authentication pages */}
                <AuthenticationRoutes />

                {/* Route for login */}
                <LoginRoutes />

                {/* Routes for main layouts (protected) */}
                <MainRoutes />
            </React.Fragment>
        </Switch>
    );
};

export default Routes;
