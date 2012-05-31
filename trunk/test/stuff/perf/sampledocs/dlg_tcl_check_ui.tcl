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

# dlg_tcl_check_ui.tcl --
#
# UI generated by GUI Builder v1.0 on 2002-09-12 10:12:04 from:
#	C:/p4/depot/main/Apps/Komodo-devel/src/samples/dlg_tcl_check.ui
# THIS IS AN AUTOGENERATED FILE AND SHOULD NOT BE EDITED.
# The associated callback file should be modified instead.
#

# Declare the namespace for this dialog
namespace eval dlg_tcl_check {}

# dlg_tcl_check::ui --
#
#   Create the UI for this dialog.
#
# ARGS:
#   root     the parent window for this form
#   args     a catch-all for other args, but none are expected
#
proc dlg_tcl_check::ui {root args} {
    # this handles '.' as a special case
    set base [expr {($root == ".") ? "" : $root}]
    variable ROOT $root
    variable BASE $base


    # Widget Initialization
    checkbutton $base.checkbutton_1 \
	    -anchor w \
	    -command [namespace code [list checkbutton_1_command]] \
	    -font {{MS Sans Serif} 10 normal roman} \
	    -text {Check it out} \
	    -variable example_checkbutton
    radiobutton $base.radio \
	    -anchor w \
	    -command [namespace code [list radio_command]] \
	    -state disabled \
	    -text {Radio Radio} \
	    -value radio \
	    -variable example_radiobutton
    radiobutton $base.freedom \
	    -anchor w \
	    -command [namespace code [list freedom_command]] \
	    -state disabled \
	    -text {Radio Freedom} \
	    -value freedom \
	    -variable example_radiobutton
    radiobutton $base.liberty \
	    -anchor w \
	    -command [namespace code [list liberty_command]] \
	    -state disabled \
	    -text {Radio Liberty} \
	    -value liberty \
	    -variable example_radiobutton
    button $base.okButton \
	    -command exit \
	    -default active \
	    -font {{MS Sans Serif} 8 bold roman} \
	    -text OK \
	    -width 8
    button $base.cancelButton \
	    -command exit \
	    -font {{MS Sans Serif} 8 normal italic} \
	    -text Cancel \
	    -width 8


    # Geometry Management

    grid $base.checkbutton_1 -in $root -row 1 -column 2 \
	    -columnspan 2 \
	    -sticky ew
    grid $base.radio -in $root -row 2 -column 2 \
	    -columnspan 2 \
	    -sticky ew
    grid $base.freedom -in $root -row 3 -column 2 \
	    -columnspan 2 \
	    -sticky ew
    grid $base.liberty -in $root -row 4 -column 2 \
	    -columnspan 2 \
	    -sticky ew
    grid $base.okButton -in $root -row 6 -column 1 \
	    -columnspan 2
    grid $base.cancelButton -in $root -row 6 -column 3 \
	    -columnspan 2

    # Resize Behavior
    grid rowconfigure $root 1 -weight 0 -minsize 7 -pad 0
    grid rowconfigure $root 2 -weight 0 -minsize 2 -pad 0
    grid rowconfigure $root 3 -weight 0 -minsize 2 -pad 0
    grid rowconfigure $root 4 -weight 0 -minsize 9 -pad 0
    grid rowconfigure $root 5 -weight 1 -minsize 10 -pad 0
    grid rowconfigure $root 6 -weight 0 -minsize 28 -pad 0
    grid columnconfigure $root 1 -weight 0 -minsize 40 -pad 0
    grid columnconfigure $root 2 -weight 1 -minsize 40 -pad 0
    grid columnconfigure $root 3 -weight 1 -minsize 40 -pad 0
    grid columnconfigure $root 4 -weight 0 -minsize 40 -pad 0
}