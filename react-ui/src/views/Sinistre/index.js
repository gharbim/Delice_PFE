import React from 'react';
import PowerBIEmbed from '../../ui-component/PowerBIEmbed';

const SinistreDashboard = () => (
    <PowerBIEmbed
        title="Sinistre Power BI Report"
        embedUrl="https://app.powerbi.com/reportEmbed?reportId=55631c0a-6499-4b5b-a410-439d0900e199&autoAuth=true&pageName=ef1cc9cad99d84471c62&filterPaneEnabled=false&navContentPaneEnabled=false"
    />
);

export default SinistreDashboard;
