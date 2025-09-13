# How It Works

As noted in the readme, pyLiveKML is an implementation of Google's 
[Keyhole Markup Language](https://developers.google.com/kml/documentation/kmlreference) (KML) that enables an 
(approximately) live feed of geospatial information into [Google Earth Pro](https://www.google.com/earth/versions/) 
(GEP). GEP is updated on the fly using an implementation of the mechanism described in 
[Google's documentation](https://developers.google.com/kml/documentation/updates). KML tags are created, updated and deleted in GEP to maintain synchronization between the Python application and GEP.

# Static -vs- Dynamic Publishing

Static publishing produces a KML file that can be loaded directly into GEP, but that (as a general rule) cannot be updated via pyLiveKML once it has been opened in GEP.  The top-layer object in a static KML file will typically be a `<Document>` or `<Folder>`, or may also be a `<NetworkLink>`.

Dynamic publishing produces a KML file that can be retrieved by GEP and used to modify GEP's state.  As a general rule, in order to perform dynamic publishing, two (or more) `NetworkLink` objects must be loaded into GEP using static publishing to construct their tags. One of the `<NetworkLink>` tags hosts the other dynamically published KML objects, and the other `<NetworkLink>` tag periodically accesses a `NetworkLinkControl` object that publishes `<Update>` tags that describe how the first `<NetworkLink>` tag's contents should be manipulated.

# KML Objects

Python representations of KML objects derive from the abstract `Object` class, which in turn derives from `_BaseObject`. All of the functionality of the `Object` class is actually contained in `_BaseObject`; the only difference between the classes is that `Object` changes the value of the class variable `_suppress_id` from `False` to `True`. The class variables of `_BaseObject` are:

* `_kml_tag` : `str`

  Specifies the tag name that will be used when the object is published.

* `_kml_fields` : `tuple[_FieldDef]`

  Specifies which properties of the object should be published as simple child tags of the object's tag. It is a tuple of `_FieldDef` objects, each of which contains the Python name of the field; the KML tag name; the parser class that will/may modify any value passed to the field; and the dumper class that will be used to convert the field value into a `str` when the field is published.

* `_kml_children` : `tuple[_ChildDef]`

  Specifies which properties of the object should be published as full children of the object's tag. It is a tuple of `_ChildDef` objects, each of which contains the Python name of the field to be treated as a child. Note the distinction between **children** and **dependents**, discussed below.

* `_kml_dependents` : `tuple[_DependentDef]`

  Specifies which properties of the object should be published as dependent children of the object's tag. It is a tuple of `_DependentDef` objects, each of which contains the Python name of the field to be treated as a dependent. Note the distinction between **children** and **dependents**, discussed below.

* `_suppress_id` : `bool`

  Controls whether the instance's tag will be published with an `id` attribute.

## Children -vs- Dependents

Children and dependents are treated identically during static publishing, but differently during dynamic publishing.

During dynamic publishing, descendants are created and published at the same time as, and as child tags of, the parent; while children are published in (and as children of) `<Update>` tags that describe how the child should be created, modified or deleted.

Note that in order for KML tags to be manipulated using `<Update>` tags, it is necessary that both the parent and child tags include their `id` as an attribute.

## Publishing Methods

### Common

There are two methods of `_BaseObject` that are routinely used to publish KML objects, both statically and dynamically.

* `construct_kml(self, with_children: bool = True, with_dependents: bool = True) -> etree.Element`

  Publishes a KML object as a tag, optionally with children and/or dependents.

* `build_kml(self, root: etree.Element, with_children: bool = True, with_dependents: bool = True,) -> None`

  Publishes a KML object into an existing tag, optionally with children and/or dependents. `construct_kml` calls `build_kml` after constructing the object's root tag.

### Dynamic only

These methods are intended to be used by `Update` instances while building their KML content. They are accessible to be overridden by subclasses of `_BaseObject` specifically to make it possible to customize dynamic `Update` behaviours.

* `create_kml(self, root: etree.Element, parent: "_BaseObject") -> etree.Element`

* `change_kml(self, root: etree.Element) -> None`

* `delete_kml(self, root: etree.Element) -> None`

`NetworkLinkControl` exposes another dynamic KML publishing method, `def construct_sync(self, with_children: bool = True, with_dependents: bool = True) -> etree.Element`. It's operation is discussed [below](https://github.com/smoke-you/pyLiveKML/blob/main/docs/how-it-works.md#networklinkcontrol). `construct_sync` ultimately calls `build_kml` and the above three methods in order to publish the corresponding tags.

## Synchronization

The purpose of dynamic publishing is to synchronize the state of the Python application hosting the KML object representations with GEP. This section can be ignored for static publishing.

### Object States

In order to facilitate synchronization, each object maintains a state property `_state`, of type `ObjectState`, which enumerates possible synchronization states:

* `IDLE` - Not synchronized
* `CREATING` - Creation of the object has been requested, but not yet published.
* `CREATED` - The object has been published.
* `CHANGING` - A change to the object has been requested, but not yet published.
* `DELETE_CREATED` - Deletion of an object in CREATING or CREATED state has been requested, but not yet published.
* `DELETE_CHANGED` - An object was changed after it's deletion was requested, but not yet published.

Note that, while it is possible to directly manipulate `_state`, it is not recommended to do so - see below.

### State Management

Several methods are exposed by `_BaseObject` to facilitate state management, rather than directly altering the `_state` attribute of the objects. These methods alter the state of the target object, and potentially it's children and/or dependents, in predictable and consistent ways.

* `activate(self, value: bool, cascade: bool = False) -> None`

  Publish the object to GEP, if `value` is `True`; or delete it if `value` is `False`.

* `field_changed(self) -> None`

  Flag that a field of the object has been changed and that the change needs to be published to GEP.

* `synchronized(self)`

  Flag that the object has been synchronized with GEP.

* `force_idle(self) -> None`

  Force the object, and all of its children, to the `IDLE` (effectively, unpublished, i.e. desynchronized) state.

### NetworkLinkControl

A `NetworkLinkControl` object, or "NLC", is the primary means of performing dynamic publishing.

The NLC hosts a `Container` (which may be either a `Document` or `Folder`, in terms of concrete classes), and works to keep that `Container` synchronized with GEP. Each time the NLC's `construct_sync` method is executed, it walks the tree of it's `Container`, looking for and noting KML objects with a state that is not IDLE or CREATED. It will record no more than `update_limit` `Create`, `Change` or `Delete` operations before publishing an `<Update>` tag containing all of the synchronization updates that it has gathered. As objects are listed for synchronization, their `synchronized` method is called.

It is also possible to statically publish an NLC, using it's conventional `construct_kml` and/or `build_kml` methods. Before calling these methods, the required operations - create, change, and delete, or a custom sequence, - should first be added to the NLC's `update` attribute.

# Constructing a KML File

In order to publish KML data, it must be collected into a properly-constructed KML file. pyLiveKML includes several methods and constants for this purpose. They can be summarized as:

1. Import some references.

  ```python
  from fastapi.responses import PlainTextResponse
  from lxml import etree
  from pyLiveKML import KML_DOCTYPE, KML_HEADERS, kml_root_tag
  ```

2. Use the `kml_root_tag` method to create a tag that will host the content. Note that this method returns a tag that includes all of the namespaces identified by Google.

  ```python
  root = kml_root_tag()
  ```

3. Construct the required KML and append it to the root tag.

  ```python
  root.append(networklinkcontrol.construct_sync())
  # or
  root.append(networklinkcontrol.construct_kml())
  # or
  root.append(networklink.construct_kml())
  # or
  root.append(container.construct_kml())
  ```

4. Create the file contents. Optionally, set `pretty_print=True` to assist with readability.

  ```python
  kml_content = etree.tostring(root, doctype=KML_DOCTYPE, encoding="utf-8", pretty_print=True)
  ```

5. (Using FastAPI) return a `PlainTextResponse` containing your KML file, using `KML_HEADERS`.

  ```python
  return PlainTextResponse(content=kml_content, headers=KML_HEADERS)
  ```

# Setting up a Live Feed

In order to set up a live feed, it is necessary to load (at least) two `<NetworkLink>` tags into GEP: one tag to host live content, and the other to retrieve that content. This mechanism is detailed well in [Google's documentation](https://developers.google.com/kml/documentation/updates). It is also implemented in [the evaluation application](https://github.com/smoke-you/pyLiveKML/blob/main/evals/main.py), where the various file endpoints /loader.kml, /elements.kml and /update.kml return files that perform distinct functions.

* /loader.kml

  Delivers a KML file containing the two `<NetworkLink>` tags, named "Elements" and "Update". The "Elements" link retrieves /elements.kml once only, while the "Update" link periodically retrieves /update.kml.

* /elements.kml

  Delivers a KML file that must use a `<Container>` (a `<Document>` or `<Folder>`, as concrete subclasses) tag as it's root element. The /update.kml file will target this `<Container>` (or one or more child `<Container>`'s under it), creating new (or changing, or deleting, existing) tags under the target. As discussed [above](https://github.com/smoke-you/pyLiveKML/blob/main/docs/how-it-works.md#networklinkcontrol), target `<Container>`'s are referenced in the Python implementation of `<NetworkLinkControl>` as the objects that it is to monitor and synchronize with GEP.

* / update.kml

  Delivers a KML file containing a `<NetworkLinkControl>` tag, with it's child `<Update>` tag and a collection of `<Create>`, `<Change>` and `<Delete>` tags that describe the next synchronization update.
