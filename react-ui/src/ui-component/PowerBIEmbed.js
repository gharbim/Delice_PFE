import React, { useEffect, useRef, useState } from 'react';
import PropTypes from 'prop-types';

// material-ui
import { Box, CircularProgress } from '@material-ui/core';

// project imports
import MainCard from './cards/MainCard';

//-----------------------|| POWER BI EMBED ||-----------------------//


const PowerBIEmbed = ({ title, embedUrl, aspectRatio }) => {
    const [loading, setLoading] = useState(true);
    const containerRef = useRef(null);
    const [size, setSize] = useState({ width: 0, height: 0 });

    useEffect(() => {
        const container = containerRef.current;
        if (!container) return undefined;

        const computeSize = (containerWidth, containerHeight) => {
            if (!containerWidth || !containerHeight) return { width: 0, height: 0 };
            const containerRatio = containerWidth / containerHeight;
            if (containerRatio > aspectRatio) {
                // container is relatively wider than the report -> height is the limiting axis
                return { width: containerHeight * aspectRatio, height: containerHeight };
            }
            // container is relatively taller than the report -> width is the limiting axis
            return { width: containerWidth, height: containerWidth / aspectRatio };
        };

        const observer = new ResizeObserver(([entry]) => {
            const { width, height } = entry.contentRect;
            setSize(computeSize(width, height));
        });
        observer.observe(container);
        setSize(computeSize(container.clientWidth, container.clientHeight));

        return () => observer.disconnect();
    }, [aspectRatio]);

    return (
        <MainCard
            content={false}
            border={false}
            boxShadow={false}
            sx={{
                height: 'calc(100vh - 88px)',
                display: 'flex',
                overflow: 'hidden',
                borderRadius: 0
            }}
        >
            <Box
                ref={containerRef}
                sx={{
                    position: 'relative',
                    flexGrow: 1,
                    display: 'flex',
                    alignItems: 'center',
                    justifyContent: 'center',
                    overflow: 'hidden'
                }}
            >
                {loading && (
                    <Box
                        sx={{
                            position: 'absolute',
                            inset: 0,
                            display: 'flex',
                            alignItems: 'center',
                            justifyContent: 'center',
                            backgroundColor: 'background.paper',
                            zIndex: 1
                        }}
                    >
                        <CircularProgress />
                    </Box>
                )}
                {size.width > 0 && size.height > 0 && (
                    <iframe
                        title={title}
                        src={embedUrl}
                        width={size.width}
                        height={size.height}
                        frameBorder="0"
                        allowFullScreen
                        onLoad={() => setLoading(false)}
                        style={{ display: 'block', border: 'none' }}
                    />
                )}
            </Box>
        </MainCard>
    );
};

PowerBIEmbed.propTypes = {
    title: PropTypes.string.isRequired,
    embedUrl: PropTypes.string.isRequired,
    aspectRatio: PropTypes.number
};

PowerBIEmbed.defaultProps = {
    aspectRatio: 16 / 9
};

export default PowerBIEmbed;
