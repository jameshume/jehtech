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
ADD: import { FormsModule } from '@angular/forms';
ADD: @NGModule({
    ...
    imports: [
        ...
        FormsModule // <<< This is what you add to the module def
    ],
    ...
})
```

* `[(ngModel)]="name"` tells Angular to bind the input field to the named member of the component class. So as user modifies input contents angular will update the value of the `name` variable.
* `{{ name }}` outputs the value of the variable
* The above two points are *two way binding*. In React we would have to implement this two way binding outselves.
* `app.module.ts` tells Angular which of its modules will be used by the `app` component. To use form functionality for eg must import the module and add it to the module `imports` array as seen above.

* Tell Angular to use Bootstrap
* In `proj_root/angular.json` find `"styles": [...]` and add the BStrap css `node_modules/bootstrap/dist/css/bootstrap.min.css` before the default. [Angular workspace config offical docs](https://angular.io/guide/workspace-config).
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


## Components
Create a new component in one of two ways:

1. Using the CLI tool `ng generate component foo` from project root dir. This create the component in the `app` folder. To embed in a subdir pass in a relative path, relative to the `app` folder.  Or...
2. Do it manually (you wouldn't normally both with this I guess!):
    * Give each component own folder
    * Make folder for component under the `app` folder with the same name as the component.
    * Inside the folder create a file named `foo.component.ts`.
    * Add into the file:
```
import { Component } from '@angular/core';

@Component({
    selector: 'app-foo', // This tells Angular to recognise <app-mycomponent/> in the HTML
                         // It must be UNIQUE and not a reserved HTML tag name.
    templateUrl: './foo.component.html', // Relative to component directory
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
* Note that the CSS file for the component is *encapsulted*: this means that CSS properties defined here
  are only applied to elements in this component, not globally to all elements. TO accomplish this,
  Angular re-writes the CSS files and applies attributes to nodes in the component HTML that will map
  to the re-written style selectors so that the styles are local to that component and not global, as
  they would be if it were pure CSS.
      * This is called **view encapsulation**. It can be disabled by adding `encapsulation: ViewEncapsulation.None` to the
        component's `@Component` decorator keys. Note if you do this the CSS in the component's CSS file applies globally!

### Selectors Deep Dive
The `selector: 'app-foo'` can be any CSS selector. For exmaple if it was changed to `selector:[app-foo]`
then cannot use `<app-foo>` and must instead use `<div app-foo>` because `app-foo` is now an attribute!

The selector could also specify a class, as in `selector: '.app-foo'`. Then we would have to use
`<div class="app-foo">`!

Selecting by ID and pseudo selectors will *not* work!


### Data Binding
* How the model can output data to the view and receive updates (react to user events) from the view: communication.
  * **String Interpolation**: `{{ data }}`. `data` is any expression that can result in a string.
  * **Property Binding**: `[property]="isEnabled"`.
    * E.g. `<button [disabled]="isEnabled">My Button</button>` or even more complex, `<span [style.font-size.px]="size">FontSize: {{size}}px</span>`.
      This binds to the HTML element property the value of the variable isEnabled in whatever component is assoc with this template.
      This will mean that the view updates dynamically when the propery changes.
  * **Event Binding**: `(event)="expression"`.
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

#### Two Way Binding
* When we want to display/use the value from the model and update it as well:
  * E.g. `<input type="text" [(ngModel)]="model_variable">...`. This combines the property binding syntax and the event
    binding syntax into one expression.


## Directives
* Two types
    1. Attribute - they sit on elements just like attributes (won't create/destoy elements, just mod element properties).
    2. Structural - do the same but change the structure of the DOM around them. *Can **not** have more than one structural directive* on the same element.
        * Structural directives are preceeded with an asterisk ('*') to make it clear what they are...
* [See the docs](https://angular.io/guide/attribute-directives)

### ngIf
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
  <p>The opposite of the text in the paragraph above</p>
</ng-template>
```

### ngStyle
Use `ngStyle` to dymanically style components. This is an attribute directive, which means it doesn't add or remove elements. It
only changes the element it was placed on.

```
<p [ngStyle]="{...key/value CSS pairs...}"]>...</p>
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

### ngClass
Provide CSS classes dynamically.

Use: `<p [ngClass]="{keys: the CSS class name, values: determine whether class should be applied}">`.

E.g. `<p [bgClass]={my_css_class: shouldApplyIt()}>`.


### ngFor

Generate lists. E.g.:

```
<ul>
  <li *ngFor="let user of users">
    {{ user.name }}
    <div>
       <img [src]=user.imagePath alt="...">
    </div>
  </li>
</ul>
```

You can also get the index of the item in the iterable by doing `*ngFor="let x of y; let i = index"`. The variable `i` will now hold the index of `x` in the iterable `y`.


### Custom Attribute Directives
* Course (and docs) example is a highligher directive...
* E.g. change the background colour of the element this directive "sits" on.
    * can **inject** the element this directive sits on into the directive itself. In `constructor` arguments list the arguments we want Angular to "inject" into our component.
  
    ```
    import { Directive, ElementRef, Renderer2 } from '@angular/core';

    @Directive({
      selector: 'appBasicHighligher'
    })
    export class BasicHighligherDirective implements OnInit {
      constructor(private elRef: ElementRef, private renderer: Renderer2) {}

      ngOnInit() {
        this.renderer.setStyle(this.elRef.nativeElement, 'background-color', 'yellow');
      }
    }

    //
    // Then in a component's HTML
    //
    <p appBasicHighlighter> ... </p>
    <!--
      ^^^^^^^^^^^^^^^^^^^
      our own customer selector that will modify the elements attributes!  
    -->
    ```

* If you created the directive manually (why would you?) you must add it to `app.module.ts` and add it to the `delcarations` list.
    * Normally you should use `ng generate directive ...`
* It is best to use the **[`Renderer`](https://angular.io/api/core/Renderer2)** - don't change the native element's attributes directly. The reason this is done is that Angular doesn't always need a (complete) DOM to render elements, e.g. for test. So the rendered and `ElementRef` act as proxies for the "real" objects so that they can be used more generically.

* Custom directives can be made more interactive by using **`HostListester`** to react to events on the element the directive sits on.

    ```
    @Directive({
      selector: '...'
    })
    export class BasicHighligherDirective implements OnInit {
      constructor(private elRef: ElementRef, private renderer: Renderer2) {}
      ngOnInit() {}

      @HostListener('mouseenter') mouseover(event: Event) {
        //          ^^^^^^^^^^^^
        //          Argument is the event that the DOM node supports that you want to listen to.
        //          You can also listen to CUSTOM EVENTS.
        this.renderer.setStyle(this.elRef.nativeElement, 'background-color', 'yellow');
      }

      @HostListener('mouseleave') mouseleave(event: Event) {
        this.renderer.setStyle(this.elRef.nativeElement, 'background-color', 'transparent');
      }      
    }
    ```

* An even easier alternative to using the `Renderer2` is to use **`HostBinding`** to bind to host properties.
    ```
    @Directive({
      selector: '...'
    })
    export class BasicHighligherDirective implements OnInit {
      // @HostBinding('WHICH-PROPERTY-OF-HOST-ELEMENT-TO-BIND-TO')
      @HostBinding('style.backgroundColor') backgroundColour: string = "transparent";

      constructor() {}
      ngOnInit() {}

      @HostListener('mouseenter') mouseover(event: Event) {
        this.backgroundColor = 'blue';
      }

      @HostListener('mouseleave') mouseleave(event: Event) {
        this.backgroundColor = 'transparent';
      }      
    }
    ```

* Customer property and event binding also works with Directives, so can use, for example, custom property
  binding in the above to specify what the colour should be for the hover event. Then you bind to those properties like `<p appBasicHighligher [thePropertyName]=...>`. If you want to be able to bind to the directive name itself, as in `[appBasicHighlighter]=...` then use the directive name as an alias for the property it should effect.

## Binding To Custom Properties
### Data Flow From Parent To (Immediate) Child
* By default, all properties inside components, are only accessible inside of the component.
* Thus, you have to *be explicit* about which properties you want to be accessible from outside the component.
    * Add a decorator to the property:
      ```
      import {..., Input} from "@angular/core";

      @Component({...})
      export class MyComponent {
        @Input() myProperty: string;
      //^^^^^^^^
      //This decorator makes the property "visible" from outside of the component
      }
      ```
* Once a property is exposed as shown above, it can now be bound to:
  ```
  <app-mycomponent
    [myProperty]="..."
  >
  ```
* You can also make the bind-property name exposed to the outside world something else:
  ```
  import {..., Input} from "@angular/core";

  @Component({...})
  export class MyComponent {
      @Input("externalPropertyName") myProperty: string;
    //^^^^^^^^
    //This decorator makes the property "visible" from outside of the component but now using an ALIAS
  }

  //
  // Then in the HTML file...
  //
  <app-mycomponent [externalPropertyName]="...">
  ```
### Data Flow From (Immediate) Child To Parent
#### Emitting Events From Custom Components
* Want to be able to emmit events from the child, which the parent can then bind to, like binding to a button onClick event, for example, but for out own component and its own event:
    ```
    // In the HTML for the component that is the parent of mycomponent,
    // we'd like to bind to our componet's event like so:
    <app-mycomponent (myEvent)="onMyEventHandler($event)">

    //
    // So in the child component, mycomponent, must do this:
    import {..., Ouput, EventEmitter} from "@angular/core";
    ...
    @Component({...})
    export class MyComponent {
        @Output myEvent = new EventEmitter<THE-TYPE-OF-THE-EVENT-DATA>();
      //^^^^^^^
      // Decorator to tell Angular component outputs this EventEmitter
        ...

        onSomeEventThatThisComponentBindsTo() {
          this.myEvent.emit(DATA-TO-PASS-WITH-EVENT);
          //   ^^^^^^^^^^^^
          //   emits the event and any parent that has bound to it will receive
          //   the event.
        }
    }

    //
    // And in the parent componetn just implement onMyEventHandler() as per normal.
    ```
* `@Output()` accepts aliases in exactly the same way that `@Input()` did above.

#### Accessing the DOM
* **Local references**: In the code below the `input` tag has a local reference assigned to it called
  "myInput".
    ```
    <input
      ... some properties ...
      #myInput
    >
    ```

    * Sometimes, if the data is only to be used when a form button is pressed, for example, two-way data binding
      may potentially be overkill. Might be easier to just "grab" the value from the DOM component itself.
      * References can be used *everywhere* in the template so you can access the referenced element like so (the element
        the function receives is the raw DOM element):
          ```
          <button ... (click)="someFunc(myInput)">
          ```
      * The reference can only be used in the HTML template, unless, as you see above,
        it is passed into a function in the TS code, OR, you use **`ViewChild()`** in the component TS code.

* **@ViewChild()**
    * Gives access to a DOM element, identified by a local reference, in the component's TS code...

      > In Angular 8+, the @ViewChild() syntax which you'll see in the next lecture needs to be changed slightly:
      >
      > Instead of:
      > `@ViewChild('myInput') myInput: ElementRef;`
      > use
      > `@ViewChild('myInput', {static: true}) myInput: ElementRef;`
      >
      > The same change (add `{ static: true }` as a second argument) needs to be applied to ALL usages of `@ViewChild()` (and also `@ContentChild()` which you'll learn about later) IF you plan on accessing the selected element inside of `ngOnInit()`.
      >
      > If you DON'T access the selected element in ngOnInit (but anywhere else in your component), set `static: false` instead!
      >
      > If you're using Angular 9+, you only need to add `{ static: true }` (if needed) but not `{ static: false }`.

    *  EG:
      ```
      export class MyComponent ... {
        @ViewChild('myInput', {static: true}) myInput: ElementRef 
      }
      ```
    * Note that the element retrieved through `@ViewChild` is of type `ElementRef`, not `HTMLInputElement` as it was if the
      ref was passed into a handler from the template. Use `myInput.nativeElement` to access the DOM node.
    * **Do NOT change** the element via `ViewChild`!! This pulls the rug out from under Angular and its re-render/reconcillation process.

## Pass Children Nodes As Properties
* Content added as child nodes to your component in the form of:
    ```
    <app-mycomponent>
      <p>Some <i>child</i> nodes passed into mycomponent here</p>
      ...
    </app-mycomponent>
    ```
* By default there is no way to get the children rendered into your component: you must use **`<ng-content></ng-content>`** in
  the parent templaate to tell Angular where in the parent to render the passed-in children.
* Useful for re-usable widgets. Eg tabs - dont want to property bind the contents... want it as children.

### Access `ng-content` via `@ContentChild`
* > Use to get the first element ... matching the selector from the content DOM. If the content DOM changes, and a new child matches the selector, the property will be updated.

    ```
    // The component template
    <app-mycomponent>
      <p   #myPRef>...</p> <!-- These are the children being passed into mycomponent -->
      <!-- ^^^^^^^
           Local ref used by component
      -->
    </app-mycomponent>

    // In the component itself
    class mycomponent {
      @ContentChild('myPRef') myPRefElement: ElementRef;
      // ^^^^^^^^^^^^^^^^^^^^
      // Gets an element, identified by a local reference, from the child nodes passed into this component.
      // Content only available after content init...
    }
    ```

## Component Lifecycle
* [See the Docs!](https://angular.io/guide/lifecycle-hooks)
* You don't have to implement all (or any) of the lifecycle hooks, just the ones you need.
* Hooks:
    * **`ngOnChanges`**: Called after bound property changes
  
          > Purpose: Respond when Angular sets or resets data-bound input properties ... receives `SimpleChanges` object as arg. 
          > ...
          > Note that this happens very frequently, so any operation you perform here impacts performance significantly.
          > ...
          > Timing: Called before `ngOnInit()` (if the component has bound inputs) and whenever one or more data-bound input properties change.

          * **Class should exentend the `OnChanges` interface**
          * `SimpleChanges` gives the  (`currentValue`) and previous (`previousValue`) value as well as if its the first change (`firstChange`).
  
    * **`ngOnInit`**: Called once the component is initialised. It's not in the DOM yet, just had Angular basic init.

          > Purpose: Initialize ... component after Angular first displays the data-bound properties and sets the ... component's input properties.
          > ...
          > Timing: Called once, after the first `ngOnChanges()`. `ngOnInit()` is still called even when `ngOnChanges()` is not, 

          * **Class should exentend the `OnInit` interface**
  
    * **`ngDoCheck`**: Runs whenever change detection is run - this means it is run *a lot*!. This doesn't necessarily mean something has changed, only that an event has occurred where Angular has to check whether a change has taken place.

          > Purpose: Detect and act upon changes that Angular can't or won't detect on its own.
          > ...
          > Timing: Called immediately after ngOnChanges() on every change detection run, and immediately after ngOnInit() on the first run

          * **Class should exentend the `DoCheck` interface**

    * **`ngAfterContentInit`**: Called after content (`ng-content`) has been "projected" into a view.
        * **Class should exentend the `AfterContentInit` interface**
    * **`ngAfterContentChecked`**: Called every time the projected content (`ng-content`) has been checked.
        * **Class should exentend the `AfterContentChecked` interface**
    * **`ngAfterViewInit`**: Called after the component's view (and child views) has been initialised.
        * **Class should exentend the `AfterViewInit` interface**
        * It is only after this has been called that components have been rendered to the DOM and can be accessed via, for example, local references.
    * **`ngAfterViewChecked`**: Called every time the view (and child views) have been checked.
        * **Class should exentend the `AfterViewChecked` interface**
    * **`ngOnDestory`**

* Order
    1. Class constructor
    2. `ngOnChanges`
    3. `ngOnInit`
    4. `ngDoCheck`
       1. `ngOnChanges` (if a change occurred)
       2. `ngAfterContentChecked`
    5. `ngAfterContentInit` (called only once)
    6. `ngAfterContentChecked`
    7. `ngAfterViewChecked`
    8. `ngOnDestory`


## Using Services And Dependency Injection

* [See the docs](https://angular.io/guide/architecture-services)
* > A component can delegate certain tasks to services, such as fetching data from the server, validating user input, or logging directly to the console. By defining such processing tasks in an injectable service class, you make those tasks available to any component. You can also make your application more adaptable by injecting different providers of the same kind of service, as appropriate in different circumstances.
* A service is just a normal TypeScript class
  
```
import { Component, ...} from '@angular/core';
import { MyService } from '...';

@Component({
  ...,
  providers: [MyService]
//^^^^^^^^^^^^^^^^^^^^^^
// This is how Angular knows to inject an instance of MyService into this component  
})
class MyComponent {
  constructor(private myService: MyService) { }
  //          ^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  //          Service injection here - Angular knows because of 'providers' field in @Component decorator.

  someFunction() {
    ...
    this.myService.someFunction();
    ...
  }
}
```

* The Angular injector works **hierachically**: When a service is used by a parent and any of its descendents, they *all* receive the *same instance* of the injected service. However, if the tree is disjoint - i.e., there are independent trees (no common parent) that use the service then they will receive different instances of the service!
    * App module - *same* instance of service available application wide. (`app.module.ts` which has its own `providers` array)
    * App component - *same* instance of service available for *all components* BUT *not* for other services.
    * Any other component - *same* instance of service available for that specific component and all descendents.
* For CHILD components that wish to use the same service as its parent, keep it in the constructor and imports, just remove it from the `providers` list in the `@Component` decorator.

* Services can be *injected into services*!
    * Constructor in service with argument of another service you want to inject AND
    * Add the `@Injectable` decorator to the service class - you add this to the *receiving* services, i.e. where you want to inject and not in what is being injected.
    * Only add `@Injectable` to the service if something is going to be injected into it, otherwise you dont need it.


## Routes
* [Read the docs](https://angular.io/api/router)
* Add the, in `app.module.ts`
    * Make sure to `import { Routes } from '@angular/router';`
    * Add an array of routes

      ```
      const appRoutes: Routes = [
        { path: '', component: HomeComponent },
        { path: 'users', component: MyUserComponent },  //< Will route to yourhost/users
        ...
      ];

      ...

      @NgModule({
        ...
        imports: [
          ...
          RouterModule.forRoot(appRoutes)  //< Add this here to register your routes and the router module
          ...
        ],
        ...
      })
      ```
      
    * Routes need an **outlet: `router-outlet`**: Tell Angular where in `app.component.html` to render the pages using the **`<router-outlet></router-outlet>` directive**.

* In your views stop using `href` in links for routed pages and instead use the **`routerLink` directive** in the same way, except when clicked using this directive the page will not be fully reloaded like it would be when folling a real link.
    * E.g. `<a routerLink="/jehtech">JEHTech</a>`.
    * E.g. `<a [routerLink]="['/jehtech', 'user', 'jeh']">JEHTech</a>`, which would route to `/jehtech/user/jh`.
    * If you ommit the leading `/` it will be a relative path, as you would expect. You can even use `./` and `../`.
* To style the active link use the `routerLinkActive` directive: `<li routerLinkActive="CSS CLASS"><a routerLink="...">Blah</a></li>`. The `routerLinkActive` can be on the link itself or a parent element.
    * To avoid the root path being always matched as an active route set `[routerLinkActiveOptions]="{exact: true}"`.
* Can also **programatically route from TS code**. To do this *inject* the router into the component.
    
    ```
    import { Router, ActivatedRoute } from '@angular/router';
    ...
    export class Blah {
      constructor (private router: Router,            //< Inject router
                   private route: ActivatedRoute) {   // < Inject currently active route. This will be
      }                                               //   the route that loaded this component
      

      ...
      
      someOnEventFunction() {
        // Perhaps reach out to backend, and then navigate
        this.router.navigate([list of strings for path]);
        //                    ^^^^^^^^^^^^^^^^^^^^^^^^
        //                    Can be absolute or relative depending on whether first string starts
        //                    with a '/'. If it is relative see below...

        // Relative paths can also be specified
        this.router.navigate(['/mypath'], {relativeTo: this.route});
      }
    }
    ```

* Routes can have **dynamic** parameters:
    
    ```
    const appRoutes: Routes = [
      ...,
      { path: 'somewhere/:id', component: ...}  //< The colon makes it a dynamic path and the value
                                                //  of `id` can be retrieved later in the component.
    ];
    ```

    The component can then fetch `id` like so:

    ```
    export class ... {
      constructor(private route: ActivatedRoute) { }
      ngOnInit() {
        this.user_id = this.route.snapshot.params['id'];
        this.fragment = this.route.snapshot.fragment'
        ...
      }
      ...
    }
    ```

* Note a snag: *component reloaded from within component*: If you use a `routeLink` from a page to the same page,
  but with different parameters, the page data will NOT get updated because the component does not need to re-render
  (it is the same component)!
  The `snapshot` used in `ngOnInit` is not sufficient.
      * Need to use the `route.params` **observable**:

          ```
          this.mySubsciption = route.params.subscribe({
            next: (params: Params) => {
                this._user_id = params['id']
            }
          });
          ```

      * NOTE: Angular **automatically CLEANS UP the route subscription** for you when the component is destroyed! Otherwise
              the subscription could try to deliver events to a subscriber thast no longer exists!! For complete safety, however
              it is better to go belt-and-braces and use `ngOnDestroy` to unsubscribe.

          ```
          ngOnDestroy() {
            this.mySubsciption.unsubscribe();
          }
          ```

* You can get/set **query parameters** and **fragments** from the links.
    * Set query parameters for a link using the **`queryParams`** directive and a (single - you can only have one) fragment using **`fragment`**:

        ```
        <a
          [routerLink]="['/some', 'path']
          [queryParams]="{someProperty: someValue}"
          fragment="someFragment"
        >
        <!-- This will generate the link /some/path?someProperty:someValue#someFragment
                                                    ^^^^^^^^^^^^^^^^^^^^^^ ^^^^^^^^^^^^
                                                    From [queryParams]     From fragment
        -->
        ```

        * Can add query params and fragments *dynamically*/*programatically* like so:

          ```
          this.router.navigate(
            ['/some', 'path', id],
            {queryParams: {someProperty: someValue}},
            fragment: someFragment
          ); 
          ```

    * Get params using `this.route.snapshot.queryParams` and fragments using `this.route.snapshot.fragment`, in the same
      way as we did for `route.params`.
        * In the same way that `snapshot` had the snag when a componet navigates to itself, `queryParams` and `fragment`
          are also **observables** that you can subscribe to, to react to changed query parameters.
        * NOTE all params retrieved are strings, so may need converting to numbers, etc!


    * **Merging Query Parameters**: When navigating to other links, having followed an existing route, we may want to, for example, `preserve` the current set of query paramters and pass them on, or `merge` in some new params into the existing set. Can be done like this.
        * To change the route from one url to another, say from `/firstUrl?name=bat7` to `/secondUrl` and pass (*preserve*) the params `name=bat7` to `/secondUrl`, do:

          ```
          this.router.navigate(['/secondUrl'], { queryParamsHandling: 'preserve' });
          // Generates the link http://your-domain/secondUrl?name=bat7
          ```
        
        * To pass through the existing set, with a few more params:
  
          ```
          this.router.navigate(['/secondUrl'], { queryParams: { age: 'not-known'}, queryParamsHandling: 'merge' });
          // Generates the link http://your-domain/secondUrl?name=bat7&age=not-known
          ```

### Nested Routes
* The `<router-outlet>` in previous examples was place in the `app.component.html` file. It works for global routes. However,
  it is possible to have child routes that link to specific parents.
* The child route "mounts" the parent and then the child components. Thus the *parent also needs a `router-outlet` and the
  routes specification in `app.module.ts` needs some nesting too, for example:

     ```
     const appRoutes: Routes = [
       ...
       { path: 'myparent', component: MyParentComponent, childrenL [
          { path: ':id', component: MyChildComponent_1},
          { path: ':id/edit', component: MyChildComponent_2 }
       ]},
       ...
     ];
     ```

### Wildcard Routes

```
const appRoutes: Routes = [
  ...
  { path: 'wherever', redirectTo:'/not-found'} // Actually re-directs the URL: the browser 
                                               // will load /wherever and then be redirected
                                               // to /not-found
]
```

But, better to **catch-all** using the generic "**`**`**" route, which must be the **last** route in the table - *order is important* because routes are prarsed top-to-bottom and the first match is used.

```
const appRoutes: Routes = [
  ...
  { path: '**', redirectTo:'/not-found'} // Must be the LAST entry in the table!
]
```

> By default, Angular matches paths by prefix. That means, that the following route will match both `/recipes` and just `/` 
> 
> `{ path: '', redirectTo: '/somewhere-else' } `
> 
> Actually, Angular will give you an error here, because that's a common gotcha: This route will now ALWAYS redirect you! Why?
> 
> Since the default matching strategy is "prefix" , Angular checks if the path you entered in the URL does start with the path specified in the route. Of course every path starts with ''  (Important: That's no whitespace, it's simply "nothing").
> 
> To fix this behavior, you need to change the matching strategy to "full" :
> 
> `{ path: '', redirectTo: '/somewhere-else', pathMatch: 'full' }`
> 
> Now, you only get redirected, if the full path is ''  (so only if you got NO other content in your path in this example).
> 
> [--Ref](https://www.udemy.com/course/the-complete-guide-to-angular-2/learn/lecture/6656336#announcements)


### Exporting The Route Map As A Module
```
import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';

...
// The routing module you create
const appRoutes: Routes = [
  //... your routres here...
]

@NgModule({

})
export class AppRoutingModule {
  imports: [
      RouterModule.forRoot(appRoutes)
  ],
  exports: [
      RouterModule
  ]
}

// Then in app-module.ts, instead of having the stuff shown above, just add `AppRoutingModule` to the `imports`.
```


### Route Guards
* Functionality that is run before a route is loaded or once you want to leave a route.
    * E.g. you only want to give access to a route if the user is logged in.
    * Don't want to do this check in every component that requires it - cumbersome. Instead better to add the guards to the route specification.
* Protect route entry: use the **`canActive`* guard.
    * Create a service for the guard. For example, course used `auth-guard.service.ts`.

      ```
      import { CanActive } from '@angular/router';
      import { Observable } from 'rxjs/Observable';

      export class AuthGuardService implements CanActivate {
          canActivate(
                  route: ActivateRouteSnapshot,
                  state: RouterStateSnaphot
          ): Observable<boolean> | Promise<boolean> | boolean {
              return someOtherService.shouldRouteBeAllowed(...)
                  .then( (theResult: boolean) => {
                      if( theResult ) {
                          return true;
                      }
                      else {
                          this.router.navigate([... some path...]);
                      }
                  })
          }
      }

      //
      // Then in the Router module, modify paths like so:
      //
      { path: ..., canActive: [AuthGuardService, ...], ... }
      ```

    * To *protect children* use **`canActiveChild`**. In route table only need to specify this on parent and it can protect both the parent and the child.

* Protect route exit using a **`canDeactive`** guard (i.e. a service).