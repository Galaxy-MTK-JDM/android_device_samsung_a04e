#!/usr/bin/env -S PYTHONPATH=../../../tools/extract-utils python3
#
# SPDX-FileCopyrightText: 2025 The LineageOS Project
# SPDX-License-Identifier: Apache-2.0
#

from extract_utils.fixups_blob import (
    blob_fixup,
    blob_fixups_user_type,
)
from extract_utils.fixups_lib import (
    lib_fixup_vendorcompat,
    lib_fixups_user_type,
    libs_proto_3_9_1,
)
from extract_utils.main import (
    ExtractUtils,
    ExtractUtilsModule,
)

namespace_imports = [
    'hardware/samsung',
]

def lib_fixup_vendor_suffix(lib: str, partition: str, *args, **kwargs):
    return f'{lib}_{partition}' if partition == 'vendor' else None

lib_fixups: lib_fixups_user_type = {
    libs_proto_3_9_1: lib_fixup_vendorcompat,
    (
        'libuuid',
    ) : lib_fixup_vendor_suffix,
} # fmt: skip

blob_fixups: blob_fixups_user_type = {
 'vendor/lib64/libskeymint_cli.so': blob_fixup()
        .replace_needed('libcrypto.so', 'libcrypto-v33.so'),
   ( 
       'vendor/lib64/libskeymint10device.so',
       'vendor/bin/hw/android.hardware.security.keymint-service',
   ): blob_fixup()
        .add_needed('android.hardware.security.rkp-V3-ndk.so')
        .replace_needed('libcrypto.so', 'libcrypto-v33.so'),
   (
       'vendor/lib64/libaudioloudc.so',
       'vendor/lib/libaudioloudc.so',
       'vendor/lib64/libaudio_param_parser-vnd.so',
       'vendor/lib/libaudio_param_parser-vnd.so',
   ): blob_fixup()
        .replace_needed('libaudiotoolkit', 'libaudiotoolkit_vendor.so'),
    'vendor/lib64/libsensorndkbridge.so': blob_fixup()
        .add_needed('libshim_sensorndkbridge.so'),
    'vendor/lib64/libcameracustom.so': blob_fixup()
        .add_needed('libui_shim.so'),
   (
       'vendor/lib/libaudioprimarydevicehalifclient.so',
       'vendor/lib64/libaudioprimarydevicehalifclient.so',
   ): blob_fixup()
        .replace_needed('libaudiocustparam.so', 'libaudiocustparam_vendor.so')
        .replace_needed('libtinyalsa.so', 'libtinyalsa_vendor.so'),
   (
       'vendor/lib64/hw/audio.primary.mt6765.so',
       'vendor/lib/hw/audio.primary.mt6765.so',
   ): blob_fixup()
        .replace_needed('libaudiocomponentengine.so', 'libaudiocomponentengine_vendor.so'),
    'vendor/lib64/libsec-ril.so': blob_fixup()
        .sig_replace('80 0E 40 F9 E1 03 16 AA 82 0C 80 52 E3 03 15 AA',
                     '80 0E 40 F9 E1 03 16 AA 82 0C 80 52 03 00 80 D2'),
    'vendor/etc/init/android.hardware.security.keymint-service.rc': blob_fixup()
        .regex_replace('android.hardware.security.keymint-service', 'android.hardware.security.keymint-service.samsung'),
    'vendor/lib64/libispcameraca.so': blob_fixup()
        .sig_replace('10 8A', 'C0 8A'),
    'vendor/etc/init/vendor.mediatek.hardware.mtkpower@1.0-service.rc': blob_fixup()
        .regex_replace('media vendor_secdir', 'media')
        .regex_replace('vendor_secdir', 'camera'),
}  # fmt: skip

module = ExtractUtilsModule(
    'a04e',
    'samsung',
    namespace_imports=namespace_imports,
    blob_fixups=blob_fixups,
    lib_fixups=lib_fixups,
)

if __name__ == '__main__':
    utils = ExtractUtils.device(module)
    utils.run()
