import { Component } from '@angular/core';
import { MatButtonModule } from '@angular/material/button';
import { MatIconModule } from '@angular/material/icon';
import { MatTabsModule } from '@angular/material/tabs';
import { FuseAlertComponent, FuseAlertService } from '@tropi/components/alert';
import { FuseHighlightComponent } from '@tropi/components/highlight';
import { FuseComponentsComponent } from 'app/modules/admin/ui/tropi-components/tropi-components.component';

@Component({
    selector   : 'alert',
    templateUrl: './alert.component.html',
    styles     : [
        `
            tropi-alert {
                margin: 16px 0;
            }
        `,
    ],
    standalone : true,
    imports    : [MatIconModule, MatButtonModule, FuseHighlightComponent, MatTabsModule, FuseAlertComponent],
})
export class AlertComponent
{
    /**
     * Constructor
     */
    constructor(
        private _tropiAlertService: FuseAlertService,
        private _tropiComponentsComponent: FuseComponentsComponent,
    )
    {
    }

    // -----------------------------------------------------------------------------------------------------
    // @ Public methods
    // -----------------------------------------------------------------------------------------------------

    /**
     * Dismiss the alert via the service
     *
     * @param name
     */
    dismiss(name: string): void
    {
        // Dismiss
        this._tropiAlertService.dismiss(name);
    }

    /**
     * Show the alert via the service
     *
     * @param name
     */
    show(name: string): void
    {
        // Show
        this._tropiAlertService.show(name);
    }

    /**
     * Toggle the drawer
     */
    toggleDrawer(): void
    {
        // Toggle the drawer
        this._tropiComponentsComponent.matDrawer.toggle();
    }
}
