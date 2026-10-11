import PropTypes from 'prop-types';
import React from 'react';
import { useLocation } from 'react-router-dom';

// material-ui
import { makeStyles, useTheme } from '@material-ui/styles';
import { Avatar, Box, ButtonBase, Divider, Typography } from '@material-ui/core';

// project imports
import LogoSection from '../LogoSection';
import ProfileSection from './ProfileSection';
import menuItems from '../../../menu-items';

// assets
import { IconMenu2 } from '@tabler/icons';

// find the menu item (with its title/icon) matching the current route
const findActiveMenuItem = (items, pathname) => {
    for (const group of items) {
        if (!group.children) continue;
        for (const child of group.children) {
            if (child.type === 'item' && child.url === pathname) {
                return child;
            }
            if (child.type === 'collapse' && child.children) {
                const match = child.children.find((sub) => sub.url === pathname);
                if (match) return match;
            }
        }
    }
    return null;
};

// style constant
const useStyles = makeStyles((theme) => ({
    grow: {
        flexGrow: 1
    },
    headerAvatar: {
        ...theme.typography.commonAvatar,
        ...theme.typography.mediumAvatar,
        transition: 'all .2s ease-in-out',
        background: theme.palette.primary.light,
        color: theme.palette.primary.dark,
        '&:hover': {
            background: theme.palette.primary.dark,
            color: theme.palette.primary.light,
            boxShadow: '0 4px 10px 0 rgba(33, 150, 243, 0.35)'
        }
    },
    boxContainer: {
        width: '228px',
        display: 'flex',
        [theme.breakpoints.down('md')]: {
            width: 'auto'
        }
    }
}));

//-----------------------|| MAIN NAVBAR / HEADER ||-----------------------//

const Header = ({ handleLeftDrawerToggle }) => {
    const classes = useStyles();
    const theme = useTheme();
    const location = useLocation();

    const activeItem = findActiveMenuItem(menuItems.items, location.pathname);
    const ActiveIcon = activeItem?.icon;

    return (
        <React.Fragment>
            {/* logo & toggler button */}
            <div className={classes.boxContainer}>
                <Box component="span" sx={{ display: { xs: 'none', md: 'block' }, flexGrow: 1 }}>
                    <LogoSection />
                </Box>
                <ButtonBase sx={{ borderRadius: '12px', overflow: 'hidden' }}>
                    <Avatar variant="rounded" className={classes.headerAvatar} onClick={handleLeftDrawerToggle} color="inherit">
                        <IconMenu2 stroke={1.5} size="1.3rem" />
                    </Avatar>
                </ButtonBase>
            </div>

            {activeItem && (
                <>
                    <Divider orientation="vertical" flexItem sx={{ mx: 2.5, display: { xs: 'none', sm: 'block' } }} />
                    <Box sx={{ display: { xs: 'none', sm: 'flex' }, alignItems: 'center', gap: 1 }}>
                        {ActiveIcon && (
                            <Box
                                sx={{
                                    display: 'flex',
                                    alignItems: 'center',
                                    justifyContent: 'center',
                                    width: 34,
                                    height: 34,
                                    borderRadius: '10px',
                                    backgroundColor: theme.palette.primary.light,
                                    color: theme.palette.primary.dark
                                }}
                            >
                                <ActiveIcon stroke={1.5} size="1.2rem" />
                            </Box>
                        )}
                        <Box>
                            <Typography variant="h4" sx={{ fontWeight: 600 }}>
                                {activeItem.title}
                            </Typography>
                            {activeItem.description && (
                                <Typography variant="caption" color="textSecondary" sx={{ display: 'block', mt: -0.25 }}>
                                    {activeItem.description}
                                </Typography>
                            )}
                        </Box>
                    </Box>
                </>
            )}

            {/* spacer to push ProfileSection to the right */}
            <div className={classes.grow} />

            {/* profile */}
            <ProfileSection />
        </React.Fragment>
    );
};

Header.propTypes = {
    handleLeftDrawerToggle: PropTypes.func
};

export default Header;
