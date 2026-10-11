import React from 'react';
import { render } from '@testing-library/react';
import { Provider } from 'react-redux';
import { Router } from 'react-router-dom';
import { createStore } from 'redux';
import { createMemoryHistory } from 'history';

import GuestGuard from './GuestGuard';

it('keeps logged-in users on the register page instead of redirecting to dashboard', () => {
    const history = createMemoryHistory({ initialEntries: ['/register'] });
    const store = createStore((state = { account: { isLoggedIn: true } }) => state);

    render(
        <Provider store={store}>
            <Router history={history}>
                <GuestGuard>
                    <div>auth content</div>
                </GuestGuard>
            </Router>
        </Provider>
    );

    expect(history.location.pathname).toBe('/register');
});
