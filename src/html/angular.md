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


