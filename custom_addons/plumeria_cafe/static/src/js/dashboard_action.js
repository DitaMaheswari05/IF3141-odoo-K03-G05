/** @odoo-module **/
import { Component, xml } from "@odoo/owl";
import { registry } from "@web/core/registry";

export class PlumeriaDashboard extends Component {
    static template = xml`
        <div style="height: calc(100vh - 116px); overflow: hidden;">
            <iframe
                src="/plumeria/dashboard"
                style="width: 100%; height: 100%; border: none; display: block;"
            />
        </div>
    `;
}

registry.category("actions").add("plumeria_cafe.dashboard_action", PlumeriaDashboard);
