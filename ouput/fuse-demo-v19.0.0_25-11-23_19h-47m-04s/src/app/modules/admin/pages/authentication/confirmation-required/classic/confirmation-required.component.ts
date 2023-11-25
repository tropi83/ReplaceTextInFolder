import { Component, ViewEncapsulation } from '@angular/core';
import { RouterLink } from '@angular/router';
import { tropiAnimations } from '@tropi/animations';

@Component({
    selector     : 'confirmation-required-classic',
    templateUrl  : './confirmation-required.component.html',
    encapsulation: ViewEncapsulation.None,
    animations   : tropiAnimations,
    standalone   : true,
    imports      : [RouterLink],
})
export class ConfirmationRequiredClassicComponent
{
    /**
     * Constructor
     */
    constructor()
    {
    }
}
