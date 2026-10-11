import React from 'react';
import { Link as RouterLink } from 'react-router-dom';

// Material UI
import { Box, Card, CardActionArea, CardContent, Grid, Typography } from '@material-ui/core';

import {
    IconDashboard,
    IconFileText,
    IconFileX,
} from '@tabler/icons';

// Project imports
const REPORTING = [ { id: 'default', title: 'Production 1', description: 'Tableau de bord Production 1.', url: '/dashboard/default', icon: IconDashboard }, { id: 'emission', title: 'Production 2', description: 'Tableau de bord Production 2.', url: '/dashboard/emission', icon: IconFileText }, { id: 'annulation', title: 'Arrêts', description: 'Tableau de bord des arrêts de production.', url: '/dashboard/annulation', icon: IconFileX } ];

const OfferingCard = ({ item, color }) => {
    const Icon = item.icon;

    return (
        <Card
            variant="outlined"
            sx={{
                height: '100%',
                borderColor: `${color}33`,
                transition: 'all .15s ease-in-out',
                '&:hover': {
                    borderColor: color,
                    boxShadow: `0 6px 18px 0 ${color}26`,
                    transform: 'translateY(-2px)'
                }
            }}
        >
            <CardActionArea
                component={RouterLink}
                to={item.url}
                sx={{ height: '100%', p: 2 }}
            >
                <CardContent sx={{ p: 0 }}>
                    <Box
                        sx={{
                            width: 40,
                            height: 40,
                            borderRadius: '10px',
                            display: 'flex',
                            alignItems: 'center',
                            justifyContent: 'center',
                            backgroundColor: `${color}1F`,
                            mb: 1.5
                        }}
                    >
                        <Icon stroke={1.5} size="1.3rem" color={color} />
                    </Box>

                    <Typography variant="subtitle1" sx={{ fontWeight: 600 }}>
                        {item.title}
                    </Typography>

                    <Typography variant="body2" color="textSecondary">
                        {item.description}
                    </Typography>
                </CardContent>
            </CardActionArea>
        </Card>
    );
};

const SectionLabel = ({ children, color }) => (
    <Box
        sx={{
            display: 'flex',
            alignItems: 'center',
            gap: 1.25,
            mb: 2
        }}
    >
        <Box
            sx={{
                width: 6,
                height: 22,
                borderRadius: '4px',
                backgroundColor: color
            }}
        />

        <Typography variant="subtitle1" sx={{ fontWeight: 700 }}>
            {children}
        </Typography>
    </Box>
);

const Accueil = () => {
    return (
        <Box>
            <SectionLabel color="#2DCFFF">
                Reporting
            </SectionLabel>

            <Grid container spacing={2} sx={{ mb: 4 }}>
                {REPORTING.map((item) => (
                    <Grid
                        item
                        xs={12}
                        sm={6}
                        md={4}
                        lg={2}
                        key={item.url}
                    >
                        <OfferingCard item={item} color="#2DCFFF" />
                    </Grid>
                ))}
            </Grid>

        </Box>
    );
};

export default Accueil;