/* Copyright (c) 2009 ActiveState Software Inc.
   See the file LICENSE.txt for licensing information. */

/* "Go To File" dialog for quickly opening a file. */

//---- globals

var log = ko.logging.getLogger("gotofile");

var gWidgets = null;
var gUIDriver = null;  // FastOpenUIDriver instance (implements koIFastOpenUIDriver)
var gSession = null;   // koIFastOpenSession
var gSep = null;       // path separator for this platform
var gOsPath = null;

var _gCurrQuery = null; // the query string last used to search
var _gIsMac = navigator.platform.match(/^Mac/);
var gOpenerKo;


//---- routines called by dialog

function onLoad()
{
    try {
        gOpenerKo = window.arguments[0].ko;
    } catch(ex) {
        log.exception("gotofile.js: onLoad failed: " + ex);
        gOpenerKo = opener.ko;
    }
    try {
        gWidgets = {
            query: document.getElementById("query"),
            throbber: document.getElementById("throbber"),
            results: document.getElementById("results"),
            statusbarPath: document.getElementById("statusbar-path"),
            statusbarNote: document.getElementById("statusbar-note")
        }
        gWidgets.statusbarNote.label = ("(" + (_gIsMac ? "Cmd" : "Ctrl")
            + "+Enter to open in Places)");
        
        var osSvc = Components.classes["@activestate.com/koOs;1"]
            .getService(Components.interfaces.koIOs);
        gSep = osSvc.sep;
        gOsPath = Components.classes["@activestate.com/koOsPath;1"]
            .getService(Components.interfaces.koIOsPath);
        
        var foSvc = Components.classes["@activestate.com/koFastOpenService;1"]
            .getService(Components.interfaces.koIFastOpenService);
        gSession = foSvc.getSession(new FastOpenUIDriver());
        
        // Configure the session.
        var partSvc = Components.classes["@activestate.com/koPartService;1"]
                .getService(Components.interfaces.koIPartService);
        gSession.setCurrProject(partSvc.currentProject);
        var openViews = [];
        var hist = gOpenerKo.views.manager.topView.viewhistory;
        //hist._debug_recentViews();
        for (var view in hist.genRecentViews()) {
            openViews.push(view);
        }
        if (gOpenerKo.places) {
            gSession.setCurrentPlace(gOpenerKo.places.manager.currentPlace);
        }
        gSession.setOpenViews(openViews.length, openViews);
        gSession.setCurrHistorySession(gOpenerKo.history.curr_session_name());

        gWidgets.query.focus();
        findFiles(gWidgets.query.value);
    } catch(ex) {
        log.exception(ex, "error loading gotofile dialog");
    }
    window.getAttention();
}

function onUnload()
{
    try {
        if (gSession) {
            gSession.abortSearch();
        }
    } catch(ex) {
        log.exception(ex, "error unloading gotofile dialog");
    }
}
 

function handleDblClick() {
    if (_openSelectedHits()) {
        window.close();
    }
}


function handleWindowKeyPress(event) {
    if (event.keyCode == KeyEvent.DOM_VK_ENTER
        || event.keyCode == KeyEvent.DOM_VK_RETURN)
    {
        _handleEnter();
    } else if (event.keyCode == KeyEvent.DOM_VK_ESCAPE) {
        window.close();
    }
    //TODO: Cmd+W / Ctrl+W: see Todd's code for plat determination
}


var _gIgnoreNextFindFiles = false;
function handleQueryKeyPress(event) {
    var index;
    var keyCode = event.keyCode;
    if (keyCode == KeyEvent.DOM_VK_ENTER
        || keyCode == KeyEvent.DOM_VK_RETURN)
    {
        if (_gIsMac && event.metaKey || event.ctrlKey) {
            _handleAlternativeEnter();
        } else {
            _handleEnter();
        }
        event.preventDefault();
        event.stopPropagation();
    } else if (keyCode == KeyEvent.DOM_VK_UP && event.shiftKey) {
        index = gWidgets.results.currentIndex - 1;
        if (index >= 0) {
            _extendSelectTreeRow(gWidgets.results, index);
        }
        event.preventDefault();
        event.stopPropagation();
    } else if (keyCode == KeyEvent.DOM_VK_DOWN && event.shiftKey) {
        index = gWidgets.results.currentIndex + 1;
        if (index < 0) {
            index = 0;
        }
        if (index < gWidgets.results.view.rowCount) {
            _extendSelectTreeRow(gWidgets.results, index);
        }
        event.preventDefault();
        event.stopPropagation();
    } else if (keyCode == KeyEvent.DOM_VK_TAB && event.shiftKey) {
        _completeSelectionOrMove(false, true);
        event.preventDefault();
        event.stopPropagation();
    } else if (keyCode == KeyEvent.DOM_VK_TAB) {
        _completeSelectionOrMove(true, true);
        event.preventDefault();
        event.stopPropagation();
    } else if (keyCode == KeyEvent.DOM_VK_UP
            /* Ctrl+p for Emacs-y people. */
            || (event.ctrlKey && event.charCode === 112)) {
        index = gWidgets.results.currentIndex - 1;
        if (index >= 0) {
            _selectTreeRow(gWidgets.results, index);
        } else if (index == -1) {
            _selectTreeRow(gWidgets.results, gWidgets.results.view.rowCount - 1);
        }
        event.preventDefault();
        event.stopPropagation();
    } else if (keyCode == KeyEvent.DOM_VK_DOWN
            /* Ctrl+n for Emacs-y people. */
            || (event.ctrlKey && event.charCode === 110)) {
        index = gWidgets.results.currentIndex + 1;
        if (index < 0) {
            index = 0;
        }
        if (index < gWidgets.results.view.rowCount) {
            _selectTreeRow(gWidgets.results, index);
        } else {
            _selectTreeRow(gWidgets.results, 0);
        }
        event.preventDefault();
        event.stopPropagation();
    }
    //TODO: page up/down
}

function findFiles(query) {
    if (!_gIgnoreNextFindFiles) {
        _gCurrQuery = query;
        gSession.findFiles(query);
    }
}




//---- UI driver class

function FastOpenUIDriver() {
}
FastOpenUIDriver.prototype.constructor = FastOpenUIDriver;

FastOpenUIDriver.prototype.QueryInterface = function (iid) {
    if (!iid.equals(Components.interfaces.koIFastOpenUIDriver) &&
        !iid.equals(Components.interfaces.nsISupports)) {
        throw Components.results.NS_ERROR_NO_INTERFACE;
    }
    return this;
}

FastOpenUIDriver.prototype.setTreeView = function(view) {
    gWidgets.results.treeBoxObject.view = view;
}


FastOpenUIDriver.prototype.setCurrPath = function(path) {
    gWidgets.statusbarPath.label = path;
}

FastOpenUIDriver.prototype.searchStarted = function() {
    _startThrobber();
}
FastOpenUIDriver.prototype.searchAborted = function() {
    if (window.document) {
        _stopThrobber();
    }
}
FastOpenUIDriver.prototype.searchCompleted = function() {
    if (window.document) {
        _stopThrobber();
    }
}



//---- internal support routines

function _startThrobber() {
    gWidgets.throbber.setAttribute("busy", "true");
}

function _stopThrobber() {
    gWidgets.throbber.removeAttribute("busy");
}

function _extendSelectTreeRow(tree, index) {
    tree.view.selection.rangedSelect(index, index, true);
    tree.treeBoxObject.ensureRowIsVisible(index);
}

function _selectTreeRow(tree, index) {
    tree.view.selection.select(index);
    tree.treeBoxObject.ensureRowIsVisible(index);
}

/* Handle <Enter> (or <Return>) being pressed to use the current
 * filter/selection state.
 */
function _handleEnter() {
    if (gWidgets.query.value != _gCurrQuery) {
        // The current set of results in now invalid. Need to get the first
        // new hit, if any, from the new query.
        // Only wait for a few seconds (don't want to hang on this).
        var hit = gSession.findFileSync(gWidgets.query.value, 3.0);
        if (! hit) {
            // No hit - this will leave the window open.
            findFiles(gWidgets.query.value);
        } else if (_openHits([hit])) {
            _gIgnoreNextFindFiles = true;  // Cancel all coming `findFiles`.
            window.close();
        } 
    } else if (_openSelectedHits()) {
        _gIgnoreNextFindFiles = true;  // Cancel all coming `findFiles`.
        window.close();
    }
}

/* Handle <Ctrl+Enter> (<Cmd+Enter> on Mac) being pressed to use the current
 * filter/selection state: open in places.
 */
function _handleAlternativeEnter() {
    if (gWidgets.query.value != _gCurrQuery) {
        // The current set of results in now invalid. Need to get the first
        // new hit, if any, from the new query.
        // Only wait for a few seconds (don't want to hang on this).
        var hit = gSession.findFileSync(gWidgets.query.value, 3.0);
        if (! hit) {
            // No hit - this will leave the window open.
            findFiles(gWidgets.query.value);
        } else {
            _openHitInPlaces(hit);
            _gIgnoreNextFindFiles = true;  // Cancel all coming `findFiles`.
            window.close();
        } 
    } else {
        _openFirstSelectedHitInPlaces();
        _gIgnoreNextFindFiles = true;  // Cancel all coming `findFiles`.
        window.close();
    }
}

function _openFirstSelectedHitInPlaces() {
    var selectedHits = gWidgets.results.view.getSelectedHits({})
    if (selectedHits.length) {
        _openHitInPlaces(selectedHits[0]);
    }
}

/* Open the given hit in Places.
 *
 * @param {koIFastOpenHit} hit The hit to open.
 */
function _openHitInPlaces(hit) {
    if (!gOpenerKo.places) {
        return;
    }
    var dir, baseName;
    if (hit.isdir) {
        dir = hit.path;
    } else {
        dir = hit.dir;
        baseName = hit.base;
    }
    gOpenerKo.places.manager.openDirectory(dir, baseName);
}

/* Open the views/paths selected in the results tree.
 *
 * @returns {Boolean} True iff successfully opened/switched-to files/tabs.
 *      For example, this returns false for a selected dir -- which isn't opened
 *      but set into the query box.
 */
function _openSelectedHits() {
    return _openHits(gWidgets.results.view.getSelectedHits({}));
}

/* Open the given hits.
 *
 * @param hits {list of koIFastOpenHit} The hits to open.
 * @returns {Boolean} True iff successfully opened/switched-to files/tabs.
 *      For example, this returns false for a selected dir -- which isn't opened
 *      but set into the query box.
 */
function _openHits(hits) {
    var hit, viewType, tabGroup;
    var fileUrlsToOpen = [];
    var dirsToOpen = [];
    for (var i in hits) {
        var hit = hits[i];
        if (hit.isdir) {
            dirsToOpen.push(gSession.relavatizePath(hit.path));
        } else if (hit.type == "open-view") {
            hit.view.makeCurrent();
        } else {
            //TODO: For history hits could perhaps restore viewType. Would need
            // changes to the back end for that.
            fileUrlsToOpen.push(ko.uriparse.pathToURI(hit.path));
        }
    }
    if (fileUrlsToOpen.length) {
        gOpenerKo.open.multipleURIs(fileUrlsToOpen);
    } else if (dirsToOpen.length) {
        // Selecting a dir should just enter that dir into the filter box.
        gWidgets.query.value = dirsToOpen[0] + gSep;
        findFiles(gWidgets.query.value);
        return false;
    }
    return true;
}


/* Complete the currently selected item in the results tree.
 * This is typically hooked up to <Tab>. Its main usefulness is in descending
 * into the currently matching directory in path mode.
 *
 * If zero or more than one items are selected in the results tree, then
 * this is no-op.
 *
 * @param {Boolean} moveForward Whether to move forward in the list. I.e. if
 *      this is false, then move backwards.
 * @param {Boolean} allowAdvance Whether to allow advancing.
 */
function _completeSelectionOrMove(moveForward, allowAdvance) {
    var hits = gWidgets.results.view.getSelectedHits(new Object());
    if (hits.length != 1) {
        return null;
    }
    var hit = hits[0];
    
    // Determine the new value to which to complete.
    var currValue = gWidgets.query.value;
    var newValue = gOsPath.join(
            gOsPath.dirname(gWidgets.query.value), hit.base);
    if (hit.isdir) {
        // Selecting a dir should just enter that dir into the filter box.
        newValue = gSession.relavatizePath(hit.path) + gSep;
    }

    // If the new value we'd complete to is already the selected value then
    // advance to the next result.
    if (allowAdvance && newValue == currValue) {
        var index;
        if (moveForward) {
            index = gWidgets.results.currentIndex + 1;
            if (index < 0) {
                index = 0;
            }
            if (index < gWidgets.results.view.rowCount) {
                _selectTreeRow(gWidgets.results, index);
            }
        } else {
            index = gWidgets.results.currentIndex - 1;
            if (index >= 0) {
                _selectTreeRow(gWidgets.results, index);
            }
        }
        // `allowAdvance=false` to not jump over multiple entries with the
        // same basename (e.g. all the "Conscript" files in Komodo source tree).
        return _completeSelectionOrMove(moveForward, false);
    }

    // Set the new value. If it is a dir, then descend into it.
    gWidgets.query.value = _gCurrQuery = newValue;
    if (hit.isdir) {
        findFiles(newValue);
    }
    return null;
}

