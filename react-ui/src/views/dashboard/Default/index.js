import React from 'react';
import PowerBIEmbed from '../../../ui-component/PowerBIEmbed';

const Dashboard = () => (
    <PowerBIEmbed
        title="Power BI Report"
        embedUrl="https://app.powerbi.com/reportEmbed?reportId=3578e9f7-3211-4d0e-93de-cb9c3390818d&autoAuth=true&pageName=ReportSection&filterPaneEnabled=false&navContentPaneEnabled=false"    />
);

export default Dashboard;
