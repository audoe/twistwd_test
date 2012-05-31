@echo off

rem ***** BEGIN LICENSE BLOCK *****
rem Version: MPL 1.1/GPL 2.0/LGPL 2.1
rem 
rem The contents of this file are subject to the Mozilla Public License
rem Version 1.1 (the "License"); you may not use this file except in
rem compliance with the License. You may obtain a copy of the License at
rem http://www.mozilla.org/MPL/
rem 
rem Software distributed under the License is distributed on an "AS IS"
rem basis, WITHOUT WARRANTY OF ANY KIND, either express or implied. See the
rem License for the specific language governing rights and limitations
rem under the License.
rem 
rem The Original Code is Komodo code.
rem 
rem The Initial Developer of the Original Code is ActiveState Software Inc.
rem Portions created by ActiveState Software Inc are Copyright (C) 2000-2007
rem ActiveState Software Inc. All Rights Reserved.
rem 
rem Contributor(s):
rem   ActiveState Software Inc
rem 
rem Alternatively, the contents of this file may be used under the terms of
rem either the GNU General Public License Version 2 or later (the "GPL"), or
rem the GNU Lesser General Public License Version 2.1 or later (the "LGPL"),
rem in which case the provisions of the GPL or the LGPL are applicable instead
rem of those above. If you wish to allow use of your version of this file only
rem under the terms of either the GPL or the LGPL, and not to allow others to
rem use your version of this file under the terms of the MPL, indicate your
rem decision by deleting the provisions above and replace them with the notice
rem and other provisions required by the GPL or the LGPL. If you do not delete
rem the provisions above, a recipient may use your version of this file under
rem the terms of any one of the MPL, the GPL or the LGPL.
rem 
rem ***** END LICENSE BLOCK *****

rem This is a slightly modified version of mozilla-build\start-msvc8.bat:
rem - don't start "msys\bin\bash"
rem - add some extra paths
echo ================ setup Mozilla/MSVC8 build env ===================


rem Keep guess-msvc.bat from trouncing the current PATH.
set MOZ_NO_RESET_PATH=1


SET MOZ_MSVCVERSION=8

if "x%MOZILLABUILD%" == "x" ( 
    set MOZILLABUILD=C:\mozilla-build
)

echo Mozilla tools directory: %MOZILLABUILD%

REM Get MSVC paths
call "%MOZILLABUILD%\guess-msvc.bat"
REM Ignore retval from guess-msvc.bat. It will return an error retval if,
REM for example, you've never had any of the Platform SDKs installed -- which
REM according to the current Mozilla Windows Build Prerequisites page is not
REM required when building with VC8 professional.
call cmd.exe /c exit 0

REM Use the "new" moztools-static
set MOZ_TOOLS=%MOZILLABUILD%\moztools

rem append moztools to PATH
SET PATH=%PATH%;%MOZ_TOOLS%\bin

rem Other PATH additions.
rem - not sure make 3.81 is necessary but probably is
rem - msys\local\bin to get iconv.exe
set PATH=%MOZILLABUILD%\make-3.81\bin;%PATH%
set PATH=%MOZILLABUILD%\msys\local\bin;%PATH%
set PATH=%MOZILLABUILD%\info-zip;%PATH%
set PATH=%MOZILLABUILD%\msys\bin;%PATH%


if "%VC8DIR%"=="" (
    if "%VC8EXPRESSDIR%"=="" (
        ECHO "Microsoft Visual C++ version 8 was not found. Exiting."
        pause
        EXIT /B 1
    )

    if "%SDKDIR%"=="" (
        ECHO "Microsoft Platform SDK was not found. Exiting."
        pause
        EXIT /B 1
    )

    rem Prepend MSVC paths
    call "%VC8EXPRESSDIR%\Bin\vcvars32.bat"

    SET USESDK=1
    rem Don't set SDK paths in this block, because blocks are early-evaluated.

    rem Fix problem with VC++Express Edition
    if "%SDKVER%"=="6" (
        rem SDK Ver.6.0 (Windows Vista SDK) and 6.1 (Windows Server 2008 SDK)
        rem does not contain ATL header files too.
        rem It is needed to use Platform SDK's ATL header files.
        SET USEPSDKATL=1

        rem SDK ver.6.0 does not contain OleAcc.idl
        rem It is needed to use Platform SDK's OleAcc.idl
        if "%SDKMINORVER%"=="0" (
            SET USEPSDKIDL=1
        )
    )
) else (
    rem Prepend MSVC paths
    call "%VC8DIR%\Bin\vcvars32.bat"

    rem If the SDK is Win2k3SP2 or higher, we want to use it
    if %SDKVER% GEQ 5 (
      SET USESDK=1
    )
)
if "%USESDK%"=="1" (
    rem Prepend SDK paths - Don't use the SDK SetEnv.cmd because it pulls in
    rem random VC paths which we don't want.
    rem Add the atlthunk compat library to the end of our LIB
    set "PATH=%SDKDIR%\bin;%PATH%"
    set LIB=%SDKDIR%\lib;%LIB%;%MOZBUILDDIR%atlthunk_compat

    if "%USEPSDKATL%"=="1" (
        if "%USEPSDKIDL%"=="1" (
            set INCLUDE=%SDKDIR%\include;%PSDKDIR%\include\atl;%PSDKDIR%\include;%INCLUDE%
        ) else (
            set INCLUDE=%SDKDIR%\include;%PSDKDIR%\include\atl;%INCLUDE%
        )
    ) else (
        if "%USEPSDKIDL%"=="1" (
            set INCLUDE=%SDKDIR%\include;%SDKDIR%\include\atl;%PSDKDIR%\include;%INCLUDE%
        ) else (
    set INCLUDE=%SDKDIR%\include;%SDKDIR%\include\atl;%INCLUDE%
        )
    )
)

rem Force the first directory on the path to be our own custom bin directory,
rem so the build will find and use our own patch.exe.
set "PATH=%~dp0\bin-win32;%PATH%"

echo ========================== done ==================================
