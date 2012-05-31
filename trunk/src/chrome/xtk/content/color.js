/* ***** BEGIN LICENSE BLOCK *****
 * Version: MPL 1.1/GPL 2.0/LGPL 2.1
 * 
 * The contents of this file are subject to the Mozilla Public License
 * Version 1.1 (the "License"); you may not use this file except in
 * compliance with the License. You may obtain a copy of the License at
 * http://www.mozilla.org/MPL/
 * 
 * Software distributed under the License is distributed on an "AS IS"
 * basis, WITHOUT WARRANTY OF ANY KIND, either express or implied. See the
 * License for the specific language governing rights and limitations
 * under the License.
 * 
 * The Original Code is Komodo code.
 * 
 * The Initial Developer of the Original Code is ActiveState Software Inc.
 * Portions created by ActiveState Software Inc are Copyright (C) 2000-2007
 * ActiveState Software Inc. All Rights Reserved.
 * 
 * Contributor(s):
 *   ActiveState Software Inc
 * 
 * Alternatively, the contents of this file may be used under the terms of
 * either the GNU General Public License Version 2 or later (the "GPL"), or
 * the GNU Lesser General Public License Version 2.1 or later (the "LGPL"),
 * in which case the provisions of the GPL or the LGPL are applicable instead
 * of those above. If you wish to allow use of your version of this file only
 * under the terms of either the GPL or the LGPL, and not to allow others to
 * use your version of this file under the terms of the MPL, indicate your
 * decision by deleting the provisions above and replace them with the notice
 * and other provisions required by the GPL or the LGPL. If you do not delete
 * the provisions above, a recipient may use your version of this file under
 * the terms of any one of the MPL, the GPL or the LGPL.
 * 
 * ***** END LICENSE BLOCK ***** */

/* * *
 * Contributors:
 *   Shane Caraveo <shanec@activestate.com>
 */

/**
 * Common functions for color processing
 */

if (typeof(xtk) == 'undefined') {
    var xtk = {};
}
xtk.color = {};
(function() {
/**
 * RGB
 *
 * covert rgb value into a long int
 *
 * @param {Long} red
 * @param {Long} green
 * @param {Long} blue
 * @return {Long} color value
 */
this.RGB = function(r,g,b) {
  return r + g * 256 + b * 256 * 256;
}

/**
 * hexToLong
 *
 * Converts a color of the form #ffaabb to a long
 *
 * @param {String} hexstring
 * @return {Long} color value
 */
this.hexToLong =function(hexstring) {
    try {
        var r, g, b;
        r = parseInt(hexstring.substring(1, 3), 16);
        g = parseInt(hexstring.substring(3, 5), 16);
        b = parseInt(hexstring.substring(5, 7), 16);
        return this.RGB(r, g, b);
    } catch (e) {
        xtk.logging.getLogger("xtk.color").exception(e);
    }
    return null;
}

this.yellow = this.RGB(0xff, 0xff, 0x00);
this.red = this.RGB(0xff, 0x00, 0x00);
this.green = this.RGB(0x00, 0xff, 0x00);
this.blue = this.RGB(0x00, 0x00, 0xff);
this.black = this.RGB(0x00, 0x00, 0x00);
this.white = this.RGB(0xff, 0xff, 0xff);

// Functions for converting a scale between 0 and 1
// into a web RGB value.
// Adapted from Bill Chadwick's http://www.bdcc.co.uk/Gmaps/Rainbow.js
// That code is under no license, claims no copyright.

this.scaler = function() {
    this.gamma = 0.8;
    this.brightness = 0.9;  // must be between 0.0 and 1.0 inclusive
    // Chadwick uses 645.  Using 780 causes a range of 1
    // to show up as black.
    this.topScale = 680.0
}

this.scaler.prototype.Adjust = function(color, factor) {
    // determine the color intensity
    return Math.floor(255.0 * Math.pow(color * factor * this.brightness, this.gamma));
}

this.scaler.prototype.NanometerToRGB = function(nanoMetres) {
    var Red = 0.0;
    var Green = 0.0;
    var Blue = 0.0;
    var factor = 0.0;
            
    if (nanoMetres < 510) {
        if (nanoMetres >= 490) {
            // Cyan to green
            Green = 1.0;
            Blue  = (510.0 - nanoMetres) / (510.0 - 490.0);
        } else {
            Blue = 1.0;            
            if (nanoMetres >= 440) {
                // Blue to cyan
                Green = (nanoMetres - 440.0) / (490.0 - 440.0);
            } else {
                // Ultra-violet to blue
                Red  = (440.0 - nanoMetres) / (440.0 - 380.0);
            }
        }
    } else if (nanoMetres < 580) {
        // Green to yellow-orange
        Green = 1.0;
        Red  = (nanoMetres - 510.0) / (580.0 - 510.0);
    } else {
        // Yellow-orange to full red
        Red = 1.0;
        Green = (nanoMetres < 644 ?
                 (645.0 - nanoMetres) / (645.0 - 580.0) : 0.0);
    }
    
    // Condition RGB according to limits of vision
    if (nanoMetres <= 700) {
        factor = ((nanoMetres >= 420) ? 1.0 :
                  (0.3 + (0.7 * (nanoMetres - 380.0)
                           / (420.0 - 380.0))));
    } else {
	factor = ((nanoMetres <= 780.0) ?
		  0.3 + 0.7 * (780.0 - nanoMetres) / (780.0 - 700.0) :
		  0.0);
    }

    Red = this.Adjust(Red, factor);
    Green = this.Adjust(Green, factor);
    Blue = this.Adjust(Blue, factor);

    var r = "#";
    if(Red < 16)
	    r += "0";
    r += Red.toString(16);

    if(Green < 16)
	    r += "0";
    r += Green.toString(16);

    if(Blue < 16)
	    r += "0";
    r += Blue.toString(16);

    return r;
}

//pass in a number between 0 and 1 to get a color between Violet and Red
this.scaler.prototype.scaleToRGB = function(w) {
    return this.NanometerToRGB(Math.round(380.0 + (w * (this.topScale - 380.0))));
}

/**
 * Return whether this is a dark color.
 * @param {string} hexstring - Hexadecimal string of the color.
 * @returns {Boolean}
 */
this.isDark = function xtk_isDark(hexstring) {
    if (hexstring[0] == "#") {
        hexstring = hexstring.slice(1);
    }
    if (hexstring.length == "3") {
        // Support short hex strings like "fff"
        hexstring = hexstring[0] + hexstring[0] +
                    hexstring[1] + hexstring[1] +
                    hexstring[2] + hexstring[2];
    }
    var color_parts = [parseInt(hexstring.slice(0, 2), 16),
                       parseInt(hexstring.slice(2, 4), 16),
                       parseInt(hexstring.slice(4, 6), 16)];
    var dark_items = color_parts.filter(
                function(elem, index, elemlist) {
                    return elem < 128;
                });
    return dark_items.length > 1;
}

/**
 * Return whether this is a light color.
 * @param {string} hexstring - Hexadecimal string of the color.
 * @returns {Boolean}
 */
this.isLight = function xtk_isLight(hexstring) {
    return !(xtk.color.isDark(hexstring));
}

}).apply(xtk.color);
