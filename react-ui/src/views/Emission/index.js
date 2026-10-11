import React from 'react';
import PowerBIEmbed from '../../ui-component/PowerBIEmbed';

const EmissionDashboard = () => (
    <PowerBIEmbed
        title="Power BI Report"
        embedUrl="https://app.powerbi.com/reportEmbed?reportId=3578e9f7-3211-4d0e-93de-cb9c3390818d&autoAuth=true&pageName=119c88e01022870685a9&filterPaneEnabled=false&navContentPaneEnabled=false"
    />
);

export default EmissionDashboard;
