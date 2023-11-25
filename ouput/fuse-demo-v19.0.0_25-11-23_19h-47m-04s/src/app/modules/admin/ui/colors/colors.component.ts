import { Component, ViewEncapsulation } from '@angular/core';
import { MatRippleModule } from '@angular/material/core';
import { tropiAnimations } from '@tropi/animations';

@Component({
    selector     : 'colors',
    templateUrl  : './colors.component.html',
    animations   : tropiAnimations,
    encapsulation: ViewEncapsulation.None,
    standalone   : true,
    imports      : [MatRippleModule],
})
export class ColorsComponent
{
    /**
     * Constructor
     */
    constructor()
    {
    }
}
