import React, { lazy } from 'react';
import { Route } from 'react-router-dom';
import Loadable from '../ui-component/Loadable';

// Landing Page - public route, no auth required
const LandingPage = Loadable(lazy(() => import('../views/LandingPage')));

//-----------------------|| LANDING ROUTE ||-----------------------//

const LandingRoute = () => {
    return <Route exact path="/" component={LandingPage} />;
};

export default LandingRoute;
