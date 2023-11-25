import { Component } from '@angular/core';
import { MatButtonModule } from '@angular/material/button';
import { MatIconModule } from '@angular/material/icon';
import { MatTabsModule } from '@angular/material/tabs';
import { FuseAlertComponent } from '@tropi/components/alert';
import { FuseHighlightComponent } from '@tropi/components/highlight';
import { FuseNavigationItem, FuseNavigationService, FuseVerticalNavigationComponent } from '@tropi/components/navigation';
import { FuseComponentsComponent } from 'app/modules/admin/ui/tropi-components/tropi-components.component';

@Component({
    selector   : 'navigation',
    templateUrl: './navigation.component.html',
    standalone : true,
    imports    : [MatIconModule, MatButtonModule, FuseAlertComponent, FuseHighlightComponent, MatTabsModule],
})
export class NavigationComponent
{
    /**
     * Constructor
     */
    constructor(
        private _tropiNavigationService: FuseNavigationService,
        private _tropiComponentsComponent: FuseComponentsComponent,
    )
    {
    }

    // -----------------------------------------------------------------------------------------------------
    // @ Public methods
    // -----------------------------------------------------------------------------------------------------

    /**
     * Get navigation item
     *
     * @param itemId
     * @param navigationName
     */
    getNavItem(itemId, navigationName): FuseNavigationItem | null
    {
        // Get the component -> navigation data -> item
        const navComponent = this._tropiNavigationService.getComponent<FuseVerticalNavigationComponent>(navigationName);

        // Return if the navigation component does not exist
        if ( !navComponent )
        {
            return null;
        }

        // Get the navigation item
        const navigation = navComponent.navigation;
        const item = this._tropiNavigationService.getItem(itemId, navigation);
        console.log(item);
        return item;
    }

    /**
     * Update badge title
     *
     * @param itemId
     * @param navigationName
     * @param title
     */
    updateBadgeTitle(itemId, navigationName, title): void
    {
        // Get the component -> navigation data -> item
        const navComponent = this._tropiNavigationService.getComponent<FuseVerticalNavigationComponent>(navigationName);

        // Return if the navigation component does not exist
        if ( !navComponent )
        {
            return null;
        }

        // Get the navigation item, update the badge and refresh the component
        const navigation = navComponent.navigation;
        const item = this._tropiNavigationService.getItem(itemId, navigation);
        item.badge.title = title;
        navComponent.refresh();
    }

    /**
     * Toggle disabled status
     *
     * @param itemId
     * @param navigationName
     */
    toggleDisabled(itemId, navigationName): void
    {
        // Get the component -> navigation data -> item
        const navComponent = this._tropiNavigationService.getComponent<FuseVerticalNavigationComponent>(navigationName);

        // Return if the navigation component does not exist
        if ( !navComponent )
        {
            return null;
        }

        // Get the navigation item, update the badge and refresh the component
        const navigation = navComponent.navigation;
        const item = this._tropiNavigationService.getItem(itemId, navigation);
        item.disabled = !item.disabled;
        navComponent.refresh();
    }

    /**
     * Swap navigation data
     *
     * @param navigationName
     */
    swapNavigationData(navigationName): void
    {
        // Get the component -> navigation data -> item
        const navComponent = this._tropiNavigationService.getComponent<FuseVerticalNavigationComponent>(navigationName);

        // Return if the navigation component does not exist
        if ( !navComponent )
        {
            return null;
        }

        // A navigation data to replace with
        const newNavigation: FuseNavigationItem[] = [
            {
                id      : 'supported-components',
                title   : 'Supported components',
                subtitle: 'Compatible third party components',
                type    : 'group',
                icon    : 'memory',
                children: [
                    {
                        id   : 'supported-components.apex-charts',
                        title: 'ApexCharts',
                        type : 'basic',
                        icon : 'insert_chart',
                        link : '/supported-components/apex-charts',
                    },
                    {
                        id   : 'supported-components.google-maps',
                        title: 'Google Maps',
                        type : 'basic',
                        icon : 'map',
                        link : '/supported-components/google-maps',
                    },
                    {
                        id   : 'supported-components.quill-editor',
                        title: 'Quill editor',
                        type : 'basic',
                        icon : 'font_download',
                        link : '/supported-components/quill-editor',
                    },
                    {
                        id   : 'supported-components.youtube-player',
                        title: 'Youtube player',
                        type : 'basic',
                        icon : 'play_circle_filled',
                        link : '/supported-components/youtube-player',
                    },
                ],
            },
        ];

        // Replace the navigation data
        navComponent.navigation = newNavigation;
        navComponent.refresh();
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
