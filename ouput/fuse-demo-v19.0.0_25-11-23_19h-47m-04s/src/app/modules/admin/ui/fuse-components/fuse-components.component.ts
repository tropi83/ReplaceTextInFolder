import { Component, OnDestroy, OnInit, ViewChild, ViewEncapsulation } from '@angular/core';
import { MatDrawer, MatSidenavModule } from '@angular/material/sidenav';
import { RouterOutlet } from '@angular/router';
import { FuseNavigationItem, FuseVerticalNavigationComponent } from '@tropi/components/navigation';
import { FuseScrollResetDirective } from '@tropi/directives/scroll-reset';
import { FuseMediaWatcherService } from '@tropi/services/media-watcher';
import { Subject, takeUntil } from 'rxjs';

@Component({
    selector     : 'tropi-components',
    templateUrl  : './tropi-components.component.html',
    styleUrls    : ['./tropi-components.component.scss'],
    encapsulation: ViewEncapsulation.None,
    standalone   : true,
    imports      : [MatSidenavModule, FuseVerticalNavigationComponent, FuseScrollResetDirective, RouterOutlet],
})
export class FuseComponentsComponent implements OnInit, OnDestroy
{
    @ViewChild('matDrawer', {static: true}) matDrawer: MatDrawer;
    drawerMode: 'side' | 'over';
    drawerOpened: boolean;
    menuData: FuseNavigationItem[];
    private _unsubscribeAll: Subject<any> = new Subject<any>();

    /**
     * Constructor
     */
    constructor(
        private _tropiMediaWatcherService: FuseMediaWatcherService,
    )
    {
        this.menuData = [
            {
                id      : 'tropi-components.libraries',
                title   : 'Libraries',
                type    : 'group',
                children: [
                    {
                        id   : 'tropi-components.libraries.mock-api',
                        title: 'MockAPI',
                        type : 'basic',
                        link : '/ui/tropi-components/libraries/mock-api',
                    },
                ],
            },
            {
                id      : 'tropi-components.components',
                title   : 'Components',
                type    : 'group',
                children: [
                    {
                        id   : 'tropi-components.components.alert',
                        title: 'Alert',
                        type : 'basic',
                        link : '/ui/tropi-components/components/alert',
                    },
                    {
                        id   : 'tropi-components.components.card',
                        title: 'Card',
                        type : 'basic',
                        link : '/ui/tropi-components/components/card',
                    },
                    {
                        id   : 'tropi-components.components.drawer',
                        title: 'Drawer',
                        type : 'basic',
                        link : '/ui/tropi-components/components/drawer',
                    },
                    {
                        id   : 'tropi-components.components.fullscreen',
                        title: 'Fullscreen',
                        type : 'basic',
                        link : '/ui/tropi-components/components/fullscreen',
                    },
                    {
                        id   : 'tropi-components.components.highlight',
                        title: 'Highlight',
                        type : 'basic',
                        link : '/ui/tropi-components/components/highlight',
                    },
                    {
                        id   : 'tropi-components.components.loading-bar',
                        title: 'Loading Bar',
                        type : 'basic',
                        link : '/ui/tropi-components/components/loading-bar',
                    },
                    {
                        id   : 'tropi-components.components.masonry',
                        title: 'Masonry',
                        type : 'basic',
                        link : '/ui/tropi-components/components/masonry',
                    },
                    {
                        id   : 'tropi-components.components.navigation',
                        title: 'Navigation',
                        type : 'basic',
                        link : '/ui/tropi-components/components/navigation',
                    },
                ],
            },
            {
                id      : 'tropi-components.directives',
                title   : 'Directives',
                type    : 'group',
                children: [
                    {
                        id   : 'tropi-components.directives.scrollbar',
                        title: 'Scrollbar',
                        type : 'basic',
                        link : '/ui/tropi-components/directives/scrollbar',
                    },
                    {
                        id   : 'tropi-components.directives.scroll-reset',
                        title: 'ScrollReset',
                        type : 'basic',
                        link : '/ui/tropi-components/directives/scroll-reset',
                    },
                ],
            },
            {
                id      : 'tropi-components.services',
                title   : 'Services',
                type    : 'group',
                children: [
                    {
                        id   : 'tropi-components.services.config',
                        title: 'Config',
                        type : 'basic',
                        link : '/ui/tropi-components/services/config',
                    },
                    {
                        id   : 'tropi-components.services.confirmation',
                        title: 'Confirmation',
                        type : 'basic',
                        link : '/ui/tropi-components/services/confirmation',
                    },
                    {
                        id   : 'tropi-components.services.splash-screen',
                        title: 'SplashScreen',
                        type : 'basic',
                        link : '/ui/tropi-components/services/splash-screen',
                    },
                    {
                        id   : 'tropi-components.services.media-watcher',
                        title: 'MediaWatcher',
                        type : 'basic',
                        link : '/ui/tropi-components/services/media-watcher',
                    },
                ],
            },
            {
                id      : 'tropi-components.pipes',
                title   : 'Pipes',
                type    : 'group',
                children: [
                    {
                        id   : 'tropi-components.pipes.find-by-key',
                        title: 'FindByKey',
                        type : 'basic',
                        link : '/ui/tropi-components/pipes/find-by-key',
                    },
                ],
            },
            {
                id      : 'tropi-components.validators',
                title   : 'Validators',
                type    : 'group',
                children: [
                    {
                        id   : 'tropi-components.validators.must-match',
                        title: 'MustMatch',
                        type : 'basic',
                        link : '/ui/tropi-components/validators/must-match',
                    },
                ],
            },
        ];
    }

    // -----------------------------------------------------------------------------------------------------
    // @ Lifecycle hooks
    // -----------------------------------------------------------------------------------------------------

    /**
     * On init
     */
    ngOnInit(): void
    {
        // Subscribe to media query change
        this._tropiMediaWatcherService.onMediaChange$
            .pipe(takeUntil(this._unsubscribeAll))
            .subscribe(({matchingAliases}) =>
            {
                // Set the drawerMode and drawerOpened
                if ( matchingAliases.includes('md') )
                {
                    this.drawerMode = 'side';
                    this.drawerOpened = true;
                }
                else
                {
                    this.drawerMode = 'over';
                    this.drawerOpened = false;
                }
            });
    }

    /**
     * On destroy
     */
    ngOnDestroy(): void
    {
        // Unsubscribe from all subscriptions
        this._unsubscribeAll.next(null);
        this._unsubscribeAll.complete();
    }
}
