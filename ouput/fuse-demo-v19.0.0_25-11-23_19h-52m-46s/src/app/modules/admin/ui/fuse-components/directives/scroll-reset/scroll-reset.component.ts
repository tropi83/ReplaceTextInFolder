import { Component } from '@angular/core';
import { MatButtonModule } from '@angular/material/button';
import { MatIconModule } from '@angular/material/icon';
import { FuseHighlightComponent } from '@tropi/components/highlight';
import { FuseComponentsComponent } from 'app/modules/admin/ui/tropi-components/tropi-components.component';

@Component({
    selector   : 'scroll-reset',
    templateUrl: './scroll-reset.component.html',
    standalone : true,
    imports    : [MatIconModule, MatButtonModule, FuseHighlightComponent],
})
export class ScrollResetComponent
{
    /**
     * Constructor
     */
    constructor(private _tropiComponentsComponent: FuseComponentsComponent)
    {
    }

    // -----------------------------------------------------------------------------------------------------
    // @ Public methods
    // -----------------------------------------------------------------------------------------------------

    /**
     * Toggle the drawer
     */
    toggleDrawer(): void
    {
        // Toggle the drawer
        this._tropiComponentsComponent.matDrawer.toggle();
    }
}
