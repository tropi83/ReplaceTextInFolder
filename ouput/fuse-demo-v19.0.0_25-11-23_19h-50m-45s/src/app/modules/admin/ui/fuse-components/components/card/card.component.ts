import { NgIf } from '@angular/common';
import { Component } from '@angular/core';
import { MatButtonModule } from '@angular/material/button';
import { MatIconModule } from '@angular/material/icon';
import { MatTabsModule } from '@angular/material/tabs';
import { FuseCardComponent } from '@tropi/components/card';
import { FuseHighlightComponent } from '@tropi/components/highlight';
import { FuseComponentsComponent } from 'app/modules/admin/ui/tropi-components/tropi-components.component';

@Component({
    selector   : 'card',
    templateUrl: './card.component.html',
    standalone : true,
    imports    : [MatIconModule, MatButtonModule, FuseHighlightComponent, MatTabsModule, FuseCardComponent, NgIf],
})
export class CardComponent
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
