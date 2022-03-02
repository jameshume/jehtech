## Course Intro Notes

Commands:

```
npm install -g @angular/cli@latest
npm install --save bootstrap@3 (or whatever version u wanna use)
ng new my-first-app --no-strict
ng serve
```

Example:

```
// A silly little component
// app.component.ts
@Component({

})
export class AppComponent {
    name = 'James';
}

// The corresponding HTML
// app.component.html
<input type="text" [(ngModel)]="name">
<p>{{ name }}</p>

// The module def
// app.module.ts
ADD: import {FormsModule } from '@angular/forms';
ADD: @NGModule({
    ...
    imports: [
        ...
        FormsModule // <<< This is what you add to the module def
    ],
    ...
})
```

* `[(ngModel)]="name"` tells Angular to bind the input field to the name member of the component class. So as user modifies input contents angular will update the value of the `name` variable.
* `{{ name }}` outputs the value of the variable
* The above two points are *two way binding*. In React we would have to implement this two way binding outselves.
* `app.module.ts` tells Angular which of its modules will be used by the `app` component. To use form functionality for eg must import the module and add it to the module `imports` array as seen above.

* Tell Angular to use Bootstrap
* In `proj_root/angular.json` find `"styles": [...]` and add the BStrap css `node_modules/bootstrap/dist/css/bootstrap.min.css` before the default.
  * ng server will need reloading.


## Course Basics Notes
In component header:

```
@Component({
   selector: 'app-root',
   templateUrl: './app.component.html',
   styleUrls: ['./app.component.css']
})
```

The `selector` is what Angular uses to understand the tag `<app-root></app-root>`. The `templateUrl` tells
Angular where the HTML source for the component is and the same fort the `styleUrls` re CSS.

In the `src` folder `main.ts` is the entrypoint for the app, specifically the line:

```
import { AppModule } from './app/app.module';
...
platformBrowserDynamic().bootstrapModule(AppModule);
```

Then in `./app/app.module.ts` the `@NgModule` has the `bootstrap` array that lists all components that should
be known to Anglular at the time it analysers our `index.html` file.


### Components
Create a new component in one of two ways:

1. Using the CLI tool `ng generate component foo`
2. Do it manually:
    * Give each component own folder
    * Make folder for component under the `app` folder with the same name as the component.
    * Inside the folder create a file named `foo.component.ts`.
    * Add into the file:
```
import { Component } from '@angular/core';

@Component({
    selector: 'app-foo', // This tells Angular to recognise <app-mycomponent/> in the HTML
                         // It must be UNIQUE and not a reserved HTML tag name.
    templateUrl: './foo/foo.component.html',
    styleUrls: [filename1.css, ...]
})
export class FooComponent {

};
```
   * Register the new component in `app.module.ts` in the `declarations` dictionary in `@NgModule`
     and remember to include your component in this file.


* Templates can also be defined *inline* by changing `templateUrl` to `template`, which then maps
  not to a file name but a string containing HTML.
* Just how templates can be inlined, so can styles by changing `styleUrl` to `styles`.

#### Selectors Deep Dive
The `selector: 'app-foo'` can be any CSS selector. For exmaple if it was changed to `selector:[app-foo]`
then cannot use `<app-foo>` and must instead use `<div app-foo>` because `app-foo` is now an attribute!

The selector could also specify a class, as in `selector: '.app-foo'`. Then we would have to use
`<div class="app-foo">`!

Selecting by ID and pseudo selectors will *not* work!


#### Data Binding
* How the model can output data to the view and receive updates (react to user events) from the view: communication.
  * String Interpolation: `{{ data }}`. `data` is any expression that can result in a string.
  * Property Binding: `[property]="isEnabled"`.
    * E.g. `<button [disabled]="isEnabled">My Button</button>` or even more complex, `<span [style.font-size.px]="size">FontSize: {{size}}px</span>`.
      This binds to the HTML element property the value of the variable isEnabled in whatever component is assoc with this template.
      This will mean that the view updates dynamically when the propery changes.
  * Event Binding: `(event)="expression"`.
    * E.g. `<button (click)="functionNameInComponent($event)">...`
      * `$event` is the data emmitted with that event. This is the DOM event object, unlike in React where a 
        virtual event wrapper would be received.
      * eg 
        ```
        export class SomeComponent {
          ...
          functionNameInComponent(event: Event) {
            this.someVariable = (<HTMLInputElement>event.target).value;
          }
        }
        ```

Important: For Two-Way-Binding, enable the `ngModel` directive. Add the `FormsModule` to the `imports[]` array in the `AppModule`.
You then also need to add the `import from @angular/forms` in the `app.module.ts` file: `import { FormsModule } from '@angular/forms';`.

##### Two Way Binding
* When we want to display/use the value from the model and update it as well:
  * E.g. `<input type="text" [(ngModel)]="model_variable">...`. This combines the property binding syntax and the event
    binding syntax into one expression.


### Directives
#### ngIf
`ngIf` is a structural directive, which means that it changes the structure of the DOM. It can be bound to an element to
determine whether it appears in the DOM (is displayed) or not.

```
<p *ngIf="boolean-expression">Some text ... </p>
   ^
   * means it is a structural directive - it changes the structure of the DOM.
```
To add an "else" block - i.e., a DOM node that will be displayed if `boolean-expression` above is `false`, use a local reference
like so:

```
<p *ngIf="boolean-expression; else booleanExpressionWasFalse">Some text ... </p>
<ng-template #booleanExpressionWasFalse>
  <p>The oppose of the text in the paragraph above</p>
</ng-template>
```

#### ngStyle
Use `ngStyle` to dymanically style components. This is an attribute directive, which means it doesn't add or remove elements. It
only changes the element it was placed on.

```
<p [ngStyle="{...key/value CSS pairs...}"]>...</p>
   ^^^^^^^^
   ^ngStyle is a directive - its not the property we bind to
   ^
   The square brackets mean we are binding to the prpoerty **of the directive**. 
```

Eg `<p [ngStyle="{backgroundColor: getColor()}"]>...</p>`, where `getColor` is a function in the assoc. component.


Better e.g.:
```
<ul>
  <li *ngFor="let course of courses" 
  [ngStyle]="{'color': course.color, 'font-size':'24px'}"> 
    {{ course.name }}
  </li>
</ul>
```

#### ngClass
Provide CSS classes dynamically.

Use: `<p [ngClass]="{keys: the CSS class name, values: determine whether class should be applied}">`.

E.g. `<p [bgClass]={my_css_class: shouldApplyIt()}>`.


#### ngFor

Generate lists. E.g.:

```
<ul>
  <li *ngFor="let user of users">{{ user.name }}</li>
</ul>
```


