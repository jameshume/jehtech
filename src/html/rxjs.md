## Course Intro Notes
* Reactive Extensions for JS
* For async and event-based programs
* Observables *emmit* data and observers *consume* that data or handle errors
  * Function that generate values once they are subscribed to.
  * The `$` suffix indicates that the variable is an Observable.  
  * E.g. `myObservable$.subscribe(v => console.log(v))`
  * E.g. or better a function that calls a REST API and returns some data: 

```
// With no errors:
restApiFunction(...api args...).subscribe(... handler code ...);
// ^^^^^^^^^^^^^^^^^^^^^^^^^^^^ ^^^^^^^^^
// ^^^^^^^^^^^^^^^^^^^^^^^^^^^^ Subscribe to observable to exec function (API call) and get results later
// Function *returns* an observable   

// With errors (DEPRECATED in >= rxJS v7):
restApiFunction(...api args...).subscribe(
    ... => {... handle success ...},
    ... => {... handle error ...}
);

// New way to handler errros:
restApiFunction(...api args...).subscribe({
    next: => {... handle success ...},
    error: => {... handle error ...},
    complete: => {... handle completion ...}
})
```

## Observables, A Little More Detail
* Observables based on idea of Streams.
* When we create observable we pass logic of observable as a callback function to the `Observable` object. Our callback is
  only executed when someone subscribes to it.
```
import { Observable } from 'rxjs';

//
// OBSERVABLE
const myObservable$ = new Observable(subscriber => {      
    ...
    subscriber.next(... some data ...)
    ...
    subscriber.next(... some data ...)
    ..
    [ // Optionally, can call error(). Also auto-called for us if exception occurs.
        subscriber.error(new Error('Description'));
    ]
    ...
    subscriber.complete() // Complete canNOT carry a payload

    return () => {
        // Teardown logic: run when the subscription ends.
    };
});

//
// OBSERVER
const observer = {
    next: value => ... handle value ...
    ...
};

//
// SUBSCRIPTION: the callback in the observable will be run...
const subscription = myObservable$.subscribe(observer);
```

* Observables must complete by either the observable calling `complete()` or `error()` or the subscriber
  cancelling the subscription (`subscription.unsubscribe()`).
* The same observable can have multiple observers: it will run its logic independantly for each observer.
* Error, complete & unsubscribe *stop* the observable. Nothing more will be received by the observer after this.
* Marble diagrams: rxmarbles.com
* [Medium Article On Unsubscribing](https://medium.com/angular-in-depth/the-best-way-to-unsubscribe-rxjs-observable-in-the-angular-applications-d8f9aa42f6a0)
* Can subscribe without passing object, just passing handler for `next()` as a function. Shorthand.


### Hot and Cold Observables
* [Medium Article On Hot And Cold Observables](https://luukgruijs.medium.com/understanding-hot-vs-cold-observables-62d04cf92e03#:~:text=An%20Observable%20is%20cold%20when,call%20this%20behaviour%20%E2%80%9Cmulticasting%E2%80%9D.)
   > An Observable is *cold* when *data is produced inside* the Observable and the Observable is *hot* when the data is *produced outside* the Observable ... Observables are *lazy*. Observables are lazy in the sense that they *only execute values when something subscribes* to it. For each subscriber the Observable starts a new execution, resulting in the fact that the *data is not shared*. If your Observable produces a lot of different values it can happen that two Observables that subscribe at more or less the same receive two different values [e.g. observable generates random numbers] ... This is not a bad thing, you just have to be aware of this behaviour.
* *Cold* means it produces a *new source* of emmitions for *each* subscription. *Hot* observables allow all observers to see the same value of each new emission but connecting to a source *outside* of the observable.
* Cold is 'unicast', hot is 'multicast'
* An observer can change its behaviour and be hot then cold, for example.

#### Cold
* An Observable is cold when data is produced inside the Observable
* *Cold* means it produces a *new source* of emmitions for *each* subscription.
* Values emmitted *independently* of other subscriptions.
* E.g. cold observable emission sources: Set of values, HTTP requests, timer/interval etc

#### Hot
* All subscriptions share the *same* source: every new subscription is a connection to the same source!
  * The logic for the emission is placed outside of the observable - e.g. DOM onClick logic where each subscription would just connect afresh to the DOM event handler and forward the event data as a `next()` call.
```
------A--------B------C---------------D--------E------...

subscribe:-----B------C---------------D--------E------...

                        subscribe:----D--------E------...
```
* E.g. hot observable emission sources: DOM events, state, subjects (an observer and observable at same time, see later).


## Creation Functions
* [DOCS](https://rxjs.dev/guide/operators)
* `of()`, `from()`, `fromEvent()`, `interval()/timer()`, `forkJoin()`, `combineLatest()`, and more...
* A.k.a "creation operators".
* > ... creation operators are functions that can be used to create an Observable with some common predefined behavior or by joining other Observables ...

### `of()`
* Creates an observable, from a set of arguments, that emits a set of values immediately and then completes.
* E.g.
```
import { of } from "rxjs";
const myObservable$ = of('This', 'is', 'a', 'set', 'of', 'values');
myObservable$.subscribe({
    next: v => console.log(v),
    complete () => console.log("done")
});
// Outputs:
// This
// is
// a
// set
// of
// values
// done
```

### `from()`
* Like `of()` except that it converts a type into an observable, for example an array, e.g:
```
from(['This', 'is', 'a', 'set', 'of', 'values'])
//   ^
//   Note now instead of a set of arguments, the argument is an array type.
```
* Or, from a promise: `from(Promise)`. `Promise.resolve()` will means `next()` is called, and a `Promise.reject()` means `error()` is called.
```
import { from } from "rxjs";

const myPromise = new Promise(resolve, reject) => {
    resolve("Promise resolved");
});

const observableFromPromise$ = from(myPromise);
// Nothing happens yet... have to subscibe first!

observableFromPromise$.({
    next: v => console.log(v),
    complete () => console.log("done")
});
// Ouputs:
// Promise resolved
// done
```
* Or, from another observable: `from(obserableObj$)`.

### `fromEvent()`
* Create an observable from event sources such as DOM `EventTarget`, Node.js `EventEmitter`, jQuery `Events` etc...
* This is *hot* observable because it connects to an already existing event source.
```
               works like
subscribe() <-------------> addEventListener()

                 works like
unsubscribe() <-------------> removeEventListener()
```

E.g.:
```
import { fromEvent } from "rxjs";

const myBtn = document.querySelector(...);
const myBtnObervable$ = fromEvent<MouseEvent>(myBtn, 'click');
myBtnObervable.subscribe({
    next: event => ... do something with click ...
    ...
})
```

### `timeout()` and `interval()`
E.g. for timer:
```
import { timer } from "rxjs";

const myTimerObervable$ = timer<number>(timeout_in_milliseconds);
myTimerObervable.subscribe({
    next: (value) => handle timer timeout // value is 0
    ...
})
```

* For timer, once created can either wait for it to complete or call `unsubscribe()`. If it completes do not need to call `unsubscribe()`.

E.g. for timer:
```
import { interval } from "rxjs";

const myIntervalObservable$ = interval<number>(interval_in_milliseconds);
myIntervalObservable.subscribe({
    next: (value) => handle interval // value is the interval number, 0, 1, 2, ...
    ...
})
```

* For interval, *must call* `unsubscribe()`!

### `forkJoin()`
* Accepts an array of observables and subscribes to all of the observables in said array. Then waits for *all* observables to complete before emitting the **lats** values they emitted as an array.
  * E.g. Useful if calling multiple API end points and want to wait for all to complete before proceeding.
```
A---------------------------------------------A------------B-|-----
B----------------------------------1--------------2-|--------------

forkJoin([A,B]) ---------------------------------------------[B, 2]-|----
                                                             ^^^^^^
                                                             Note only the most recently seen
                                                             values from A & B are emitted: prev
                                                             values are lost!
```
* If there is an error emitted then all values are lost and only the error will be seen by the observer. All of the joined observables will be auto unsubscribed from by `forkJoin()`.
* Beware of observables that *never complete*: `forkJoin([of('ABC'), interval(1000)])` - this wont emit everything as `interval()` never `complete()`'s!


### `combineLatest()`
* Like `forkJoin()` except emitts a value every time a *set* of the joined observables emitts a value:
```
A---------------------------------------------A------------B-----------C-|--
B----------------------------------1--------------2-|-----------------------

forkJoin([A,B]) ------------------------------[A,1]--------[B,2]-|-----[C,2]
                                              ^^^^^        ^^^^^       ^^^^^
                                              We got both sets of values
```

Note, however that values can still be lost because it will wait for all observables to fire an event before combining them:
```
import { combineLatest, interval } from 'rxjs';

const o1$ = interval(1000);
const o2$ = interval(5000);

combineLatest(o1$, o2$).subscribe(([v1, v2]) => console.log(v1, v2));

// Outputs:
4 0   //<< The previous values of v1 are lost because combineLatest waits for v2 to emit a value!
5 0   //<< But after this we see all values of v1 and v2
...
9 0
9 1
10 1
...

```

* Note, unlike `forkJoin()`, with observables that never complete, like `interval()`, this function will still emit values.

### `ajax()`
```
import { ajax } from 'rxjs/ajax';

const obs$ = ajax('https://random-data-api.com/api/beer/random_beer');
obs$.subscribe((v) => console.log(v.response));
// Outputs a random beer:
// {
//    id: 5590, uid: '6aca38d0-178f-4e58-bd01-22eb6cfa58bb', brand: 'Stella Artois', name: 'Sierra Nevada Bigfoot Barleywine Style Ale', style: 'Dark Lager', …}
//    alcohol: "9.0%"
//    blg: "18.2°Blg"
//    brand: "Stella Artois"
//    ...


// ... OR even easier for JSON responses ...
const obs$ = ajax.getJSON('https://random-data-api.com/api/beer/random_beer');
obs$.subscribe((jsonObj) => console.log(jsonObj));
// Outputs a random beer's JSON like above
}

// Can also specify method, url etc...
const obs$ = ajax({
  url: ...,
  method: 'POST',
  headers: {
    ...
  },
  body: {
    ...
  }
});
```


## Pipable Operators
* Take an observable, modify its output is someway, to produce a new observable - like a *decorator* function.
* Applying a Pipeable Opertaor creates a new Observable - it does NOT modify the existing observable!

```
 +------------------+
 |   +----------+   |
 |   |  Source  |   |
 |   +-----|----+   |
 |         |        |
 |   +-----V----+   |
 |   | Operator |   |
 |   +-----|----+   |
 |         |        |
 |   +-----V----+   |
 |   | Operator |   |
 |   +-----|----+   |
 :        ...       :
 :        ...       :
 |         |        |
 |   +-----V----+   |
 |   | Operator |   |
 |   +----------+   |
 +---------|--------+
           |
     +-----V----+
     | Observer |
     +----------+
```

### `filter()`
* Passes output onwards based on predicate function passed in.
* Affects `next()` only. `error()` and `complete()` will *always* be passed straight through the filter.
```
import { filter } from "rxjs/operators";

const observable$ = new Observable(...);

observable$.pipe(
    filter(value => boolean-based-on-value-contents)
).subscribe({
    ... normal subscription callback functions ...
});
```

### `map()`
* Like `map` for arrays: maps each value emitted to another value - i.e. apply a function to each emitted value.
* Affects `next()` only. `error()` and `complete()` will *always* be passed straight through the filter.

```
import { from } from "rxjs";
import { map } from "rxjs/operators";

const myObs$ = from([1, 2, 3, 4, 5, 6]);
myObs$.pipe(
    map(value =>value * 10)
).subscribe({
    next: v => console.log(v)
});
// Outputs:
// 10
// 20
// ...
// 60
```

### `tap()`
* Like a "spy" - useful for debug - allows side effects without interacting with notifications.
* All notifications are re-emitted without modification!
* [Medium article on tap()](https://jaywoz.medium.com/information-is-king-tap-how-to-console-log-in-rxjs-7fc09db0ad5a)


### `debounceTime()`
* After x seconds of no emmissions it emits the last value seen.
* Error and complete notifications are not delayed, however, and just pased through.
```
//     source               A              B    C
//       ^                  :              :    :
//       |                  :              :    :
//  debounceTime(2000)  ----|----|----|----|----|----|----|----|....
//       ^                  1s   2s   3s   4s   5s   6s   7s   8s...
//       |                            :                   :
//   subscriber                       A                   C

import { debounceTime } from "rxjs/operators";

myObservable$.pipe(
    debounceTime(2000)
).subscribe({
    next: v => console.log(v)
});
```


### `catchError()`
* Passes `next()` and `complete()` through unchanged, but lets us specify a *fallback source* if the primary source emits an error.
  * Primary emitting error causes `catchError()` to suppress that error and instead subscribe to the fallback source and continue.
* Must return an observable.
```
import { catchError } from "rxjs/operators";

myObservable$.pipe(
    catchError(error => ... return an alternative observable ...)
).subscribe({
    next: v => console.log(v)
});
```

* To suppress the error and just complete if an error occurs `EMPTY` can be used:

```
import { EMPTY } from "rxjs";
import { catchError } from "rxjs/operators";

myObservable$.pipe(
    catchError(error => EMPTY)
).subscribe({
    next: v => console.log(v)
});
```

### Flattening Operators
* Map each value from an observable to a new inner observable, creates a subscription to the inner and pass values
  emitted by it to the output.
* Next and error notifications are passed to the output.

#### `concatMap`
* `concatMap(project: function, resultSelector: function): Observable`
* Map values to inner observable, subscribe and emit in order.
* It is given an inner observable that is subscribed to every time the out observable emits a value:
```
// -----------------------------------A-----------------B-----------------....
//                                    |                 |
// concatMap(() => newStream$)        >----1---2---|    >----1---2---|   } Values emitted by newSteam$
//                                         |   |             |   |
// ----------------------------------------1---2-------------3---4--------...
import { concatMap } from "rxjs/operators";

source$.pipe(
    concatMap( () => anotherSource$ )
).subscribe(...);
```

There is also a `resultSelector` that can be used to combine/modify/filter the values being emitted. Here is an example from [rxmarbles.com](https://rxmarbles.com/#concatMap).

NOTE that if the observable that is "passed in" to `concatMap` does not complete, subsequent emissions by the original source will not be seen! See this:

```
import { Observable, of } from 'rxjs';
import { concatMap } from 'rxjs/operators';

const source$ = new Observable((subscriber) => {
  setTimeout(() => subscriber.next('A'), 2000);
  setTimeout(() => subscriber.next('B'), 5000);
});

junk$ = new Observable((subscriber) => {
  subscriber.next(1);
  subscriber.next(2);
  subscriber.complete(); //<< If this is NOT done then the second set of 1, 2 will not be output!!
});

console.log('App has started');
source$
  .pipe(concatMap((value) => junk$))
  .subscribe((value) => console.log(value));
```

If the inner observable is slow, values emitted by the primary source whilst the secondary observable is delayed are just queued and emitted when the secondary finishes:

```
import { Observable, of } from 'rxjs';
import { concatMap } from 'rxjs/operators';

const source$ = new Observable((subscriber) => {
  setTimeout(() => {
    console.log('emitting A');
    subscriber.next('A');
  }, 1000);
  setTimeout(() => {
    console.log('emitting B');
    subscriber.next('B');
  }, 2000);
});

let junk$ = of(1, 2);
junk$ = new Observable((subscriber) => {
  subscriber.next(1);
  subscriber.next(2);
  setTimeout(() => {
    console.log('done');
    subscriber.complete();
  }, 10000);
});

console.log('App has started');
source$
  .pipe(concatMap((value) => junk$))
  .subscribe((value) => console.log(value));

// Outputs:
// emitting A
// 1
// 2
// emitting B
// ... long pause whilst the secondary observable completes ...
// done
// 1  << B was emitted and it was queued up whilst the above completed. Not lost!
// 2
// done
```

* Errors will exit the main outer subscription! `concatMap` will unsubscribe from the source for us.

#### `switchMap`
* Like `concatMap` except that it does not queue up subsequent emissions from the source observable whilst
  a previous emission is being processed by the secondary subscription it triggers. Instead it would
  unsubscribe from the secondary observable and create a new subscription.
* Dont use for POSTs. Do use for GETs.
* Here is an example from [rxmarbles.com](https://rxmarbles.com/#switchMap).

#### `mergeMap`
* Easy to create memory leaks with this!

```
---------------------------A--------------B---------------------C---------------...
                           |              |                     |
mergeMap(v => obs$()) -----+--------------+---------------------+---------------...   
                           |              |                     |
                           +--------------|--------1---...      +----3---------|     } Concurrent
                                          +--------:-----------------:------2---...  } subscriptions!
                                                   :                 :      :
---------------------------------------------------1-----------------3------2---...
```
* Because each subscription causes a concurrent inner subscription, if the inner source
  never completes memory can be chewed up at a rate of knots.

#### `exhaustMap`
TODO



## Subjects

* [Docs](https://www.learnrxjs.io/learn-rxjs/subjects/subject)
* Combination of an observer and an observable
  * You can `.subscribe()` to it and use it as a regular observable.
  * As subject is a source of emissions it behaves as a *hot observable* so all subscribers see the same values.
    * Calling `next(value)`, `error(err)` or `complete()` on a subject will *multicast* that value to all subscribers..

```
code          -----+-------------+------------+----------------x-----...
                   | next(A)     | next(B)    | next(C)        | error(err)
                   v             v            v                v
subject       -----A-------------B------------C----------------x-----...
                         |       :     |      :                :
                         |       :     |      :                :
subscriber 1             +-------B-----|------C----------------x-----...
                                       |      :                :
                                       |      :                :
subscriber 2                           +------C----------------x-----...

                         ^^^^^^^^      ^^^^^^^^
                         ^^^^^^^^      The length of time subscriber 2 has to wait, from start of subscription
                         ^^^^^^^^      before getting a value.
                         The length of time subscriber 1 has to wait, from start of subscription
                         before getting a value.

                         ^^^^^^^^^^^^^^^^^^^^^^
                         For subscribers 1 & 2 to not have to wait to get a state, and instead on subscribe
                         be called with the last seen state, use BehviorSubject
```
* E.g. multicast a button event to many listeners.
* Note that a subscriber to a `Subject` will have to wait, from point of subscribe to the next emission to
  find state. For a `BehaviorSubject` this is not the case. On subscription it gets a `.next()` call with the
  last seen state. `BehaviorSubject` needs an *initial value*:

```
code          -------------------+------------+----------------x-----...
                                 | next(C)    | next(D)        | error(err)
                                 v            v                v
BS (A)        -------------------B------------D----------------x-----...
                   |             :     |      :                :
                   |             :     |      :                :
subscriber 1       A-------------B-----|------C----------------x-----...
                   ^                   |      :                :
                   ^                   |      :                :
subscriber 2       ^                   B------C----------------x-----...
                   ^                   ^
                   ^                   On subscription the last seen value is always sent immediately.
                   ^
                   Note when BS has not received a value via `next()` it uses the initial value. 
```
