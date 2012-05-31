# ***** BEGIN LICENSE BLOCK *****
# Version: MPL 1.1/GPL 2.0/LGPL 2.1
# 
# The contents of this file are subject to the Mozilla Public License
# Version 1.1 (the "License"); you may not use this file except in
# compliance with the License. You may obtain a copy of the License at
# http://www.mozilla.org/MPL/
# 
# Software distributed under the License is distributed on an "AS IS"
# basis, WITHOUT WARRANTY OF ANY KIND, either express or implied. See the
# License for the specific language governing rights and limitations
# under the License.
# 
# The Original Code is Komodo code.
# 
# The Initial Developer of the Original Code is ActiveState Software Inc.
# Portions created by ActiveState Software Inc are Copyright (C) 2000-2007
# ActiveState Software Inc. All Rights Reserved.
# 
# Contributor(s):
#   ActiveState Software Inc
# 
# Alternatively, the contents of this file may be used under the terms of
# either the GNU General Public License Version 2 or later (the "GPL"), or
# the GNU Lesser General Public License Version 2.1 or later (the "LGPL"),
# in which case the provisions of the GPL or the LGPL are applicable instead
# of those above. If you wish to allow use of your version of this file only
# under the terms of either the GPL or the LGPL, and not to allow others to
# use your version of this file under the terms of the MPL, indicate your
# decision by deleting the provisions above and replace them with the notice
# and other provisions required by the GPL or the LGPL. If you do not delete
# the provisions above, a recipient may use your version of this file under
# the terms of any one of the MPL, the GPL or the LGPL.
# 
# ***** END LICENSE BLOCK *****

# Dialog.tcl --
#
# Generated by GUI Builder v1.0 on 2002-09-11 14:26:49 from:
#	C:/depot/main/Apps/Komodo-devel/src/samples/Dialog.ui
# This file is auto-generated.  It may be modified with the
# following restrictions:
#	1. Only code inside procs is round-tripped.
#

# Declare the namespace for this dialog
namespace eval Dialog {}

# Source the file, which must exist
source [file join [file dirname [info script]] Dialog_ui.tcl]
# Dialog::button_1_command --
#
# Here we create a command that handles the 
# -command option for the widget button_1
#
# ARGS:
#
proc Dialog::button_1_command args {}



# Standalone Code Initialization

# Dialog::init --
#
#   Call the optional userinit and initialize the dialog.
#   Do not edit this procedure.
#
# Arguments:
#   root   the root window to load this dialog into
#
# Results:
#   dialog will be created, or a background error will be thrown
#
proc Dialog::init {root args} {
    # Catch this in case the user didn't define it
    catch {Dialog::userinit}
    if {[info exists embed_args]} {
	# we are running in the plugin
	Dialog::ui $root
    } elseif {$::argv0 == [info script]} {
	# we are running in stand-alone mode
	wm title $root Dialog
	if {[catch {
	    # Create the UI
	    Dialog::ui  $root
	} err]} {
	    bgerror $err ; exit 1
	}
    }
    catch {Dialog::run $root}
}
Dialog::init .

