/* Generated file. Do not edit. */

typedef struct {
	const char *name;
	const char *docs;
} NmcPropertyDesc;

NmcPropertyDesc setting_802_11_olpc_mesh[] = {
	{ "channel", "Channel on which the mesh network to join is located." },
	{ "dhcp-anycast-address", "Anycast DHCP MAC address used when requesting an IP address via DHCP. The specific anycast address used determines which DHCP server class answers the request." },
	{ "name", "The setting's name, which uniquely identifies the setting within the connection.  Each setting type has a name unique to that type, for example \"ppp\" or \"wireless\" or \"wired\"." },
	{ "ssid", "SSID of the mesh network to join." },
};
  
NmcPropertyDesc setting_802_11_wireless[] = {
	{ "band", "802.11 frequency band of the network.  One of \"a\" for 5GHz 802.11a or \"bg\" for 2.4GHz 802.11.  This will lock associations to the Wi-Fi network to the specific band, i.e. if \"a\" is specified, the device will not associate with the same network in the 2.4GHz band even if the network's settings are compatible.  This setting depends on specific driver capability and may not work with all drivers." },
	{ "bssid", "If specified, directs the device to only associate with the given access point.  This capability is highly driver dependent and not supported by all devices.  Note: this property does not control the BSSID used when creating an Ad-Hoc network and is unlikely to in the future." },
	{ "channel", "Wireless channel to use for the Wi-Fi connection.  The device will only join (or create for Ad-Hoc networks) a Wi-Fi network on the specified channel.  Because channel numbers overlap between bands, this property also requires the \"band\" property to be set." },
	{ "cloned-mac-address", "If specified, request that the Wi-Fi device use this MAC address instead of its permanent MAC address.  This is known as MAC cloning or spoofing." },
	{ "hidden", "If TRUE, indicates this network is a non-broadcasting network that hides its SSID.  In this case various workarounds may take place, such as probe-scanning the SSID for more reliable network discovery.  However, these workarounds expose inherent insecurities with hidden SSID networks, and thus hidden SSID networks should be used with caution." },
	{ "mac-address", "If specified, this connection will only apply to the Wi-Fi device whose permanent MAC address matches. This property does not change the MAC address of the device (i.e. MAC spoofing)." },
	{ "mac-address-blacklist", "A list of permanent MAC addresses of Wi-Fi devices to which this connection should never apply.  Each MAC address should be given in the standard hex-digits-and-colons notation (eg \"00:11:22:33:44:55\")." },
	{ "mode", "Wi-Fi network mode; one of \"infrastructure\", \"adhoc\" or \"ap\".  If blank, infrastructure is assumed." },
	{ "mtu", "If non-zero, only transmit packets of the specified size or smaller, breaking larger packets up into multiple Ethernet frames." },
	{ "name", "The setting's name, which uniquely identifies the setting within the connection.  Each setting type has a name unique to that type, for example \"ppp\" or \"wireless\" or \"wired\"." },
	{ "rate", "If non-zero, directs the device to only use the specified bitrate for communication with the access point.  Units are in Kb/s, ie 5500 = 5.5 Mbit/s.  This property is highly driver dependent and not all devices support setting a static bitrate." },
	{ "seen-bssids", "A list of BSSIDs (each BSSID formatted as a MAC address like \"00:11:22:33:44:55\") that have been detected as part of the Wi-Fi network.  NetworkManager internally tracks previously seen BSSIDs. The property is only meant for reading and reflects the BSSID list of NetworkManager. The changes you make to this property will not be preserved." },
	{ "ssid", "SSID of the Wi-Fi network. Must be specified." },
	{ "tx-power", "If non-zero, directs the device to use the specified transmit power. Units are dBm.  This property is highly driver dependent and not all devices support setting a static transmit power." },
};
  
NmcPropertyDesc setting_802_11_wireless_security[] = {
	{ "auth-alg", "When WEP is used (ie, key-mgmt = \"none\" or \"ieee8021x\") indicate the 802.11 authentication algorithm required by the AP here.  One of \"open\" for Open System, \"shared\" for Shared Key, or \"leap\" for Cisco LEAP.  When using Cisco LEAP (ie, key-mgmt = \"ieee8021x\" and auth-alg = \"leap\") the \"leap-username\" and \"leap-password\" properties must be specified." },
	{ "group", "A list of group/broadcast encryption algorithms which prevents connections to Wi-Fi networks that do not utilize one of the algorithms in the list.  For maximum compatibility leave this property empty.  Each list element may be one of \"wep40\", \"wep104\", \"tkip\", or \"ccmp\"." },
	{ "key-mgmt", "Key management used for the connection.  One of \"none\" (WEP), \"ieee8021x\" (Dynamic WEP), \"wpa-none\" (Ad-Hoc WPA-PSK), \"wpa-psk\" (infrastructure WPA-PSK), or \"wpa-eap\" (WPA-Enterprise).  This property must be set for any Wi-Fi connection that uses security." },
	{ "leap-password", "The login password for legacy LEAP connections (ie, key-mgmt = \"ieee8021x\" and auth-alg = \"leap\")." },
	{ "leap-password-flags", "Flags indicating how to handle the \"leap-password\" property." },
	{ "leap-username", "The login username for legacy LEAP connections (ie, key-mgmt = \"ieee8021x\" and auth-alg = \"leap\")." },
	{ "name", "The setting's name, which uniquely identifies the setting within the connection.  Each setting type has a name unique to that type, for example \"ppp\" or \"wireless\" or \"wired\"." },
	{ "pairwise", "A list of pairwise encryption algorithms which prevents connections to Wi-Fi networks that do not utilize one of the algorithms in the list. For maximum compatibility leave this property empty.  Each list element may be one of \"tkip\" or \"ccmp\"." },
	{ "proto", "List of strings specifying the allowed WPA protocol versions to use. Each element may be one \"wpa\" (allow WPA) or \"rsn\" (allow WPA2/RSN).  If not specified, both WPA and RSN connections are allowed." },
	{ "psk", "Pre-Shared-Key for WPA networks.  If the key is 64-characters long, it must contain only hexadecimal characters and is interpreted as a hexadecimal WPA key.  Otherwise, the key must be between 8 and 63 ASCII characters (as specified in the 802.11i standard) and is interpreted as a WPA passphrase, and is hashed to derive the actual WPA-PSK used when connecting to the Wi-Fi network." },
	{ "psk-flags", "Flags indicating how to handle the \"psk\" property." },
	{ "wep-key-flags", "Flags indicating how to handle the \"wep-key0\", \"wep-key1\", \"wep-key2\", and \"wep-key3\" properties." },
	{ "wep-key-type", "Controls the interpretation of WEP keys.  Allowed values are NM_WEP_KEY_TYPE_KEY (1), in which case the key is either a 10- or 26-character hexadecimal string, or a 5- or 13-character ASCII password; or NM_WEP_KEY_TYPE_PASSPHRASE (2), in which case the passphrase is provided as a string and will be hashed using the de-facto MD5 method to derive the actual WEP key." },
	{ "wep-key0", "Index 0 WEP key.  This is the WEP key used in most networks.  See the \"wep-key-type\" property for a description of how this key is interpreted." },
	{ "wep-key1", "Index 1 WEP key.  This WEP index is not used by most networks.  See the \"wep-key-type\" property for a description of how this key is interpreted." },
	{ "wep-key2", "Index 2 WEP key.  This WEP index is not used by most networks.  See the \"wep-key-type\" property for a description of how this key is interpreted." },
	{ "wep-key3", "Index 3 WEP key.  This WEP index is not used by most networks.  See the \"wep-key-type\" property for a description of how this key is interpreted." },
	{ "wep-tx-keyidx", "When static WEP is used (ie, key-mgmt = \"none\") and a non-default WEP key index is used by the AP, put that WEP key index here.  Valid values are 0 (default key) through 3.  Note that some consumer access points (like the Linksys WRT54G) number the keys 1 - 4." },
};
  
NmcPropertyDesc setting_802_1x[] = {
	{ "altsubject-matches", "List of strings to be matched against the altSubjectName of the certificate presented by the authentication server. If the list is empty, no verification of the server certificate's altSubjectName is performed." },
	{ "anonymous-identity", "Anonymous identity string for EAP authentication methods.  Used as the unencrypted identity with EAP types that support different tunneled identity like EAP-TTLS." },
	{ "ca-cert", "Contains the CA certificate if used by the EAP method specified in the \"eap\" property. Certificate data is specified using a \"scheme\"; two are currently supported: blob and path. When using the blob scheme (which is backwards compatible with NM 0.7.x) this property should be set to the certificate's DER encoded data. When using the path scheme, this property should be set to the full UTF-8 encoded path of the certificate, prefixed with the string \"file://\" and ending with a terminating NUL byte. This property can be unset even if the EAP method supports CA certificates, but this allows man-in-the-middle attacks and is NOT recommended." },
	{ "ca-path", "UTF-8 encoded path to a directory containing PEM or DER formatted certificates to be added to the verification chain in addition to the certificate specified in the \"ca-cert\" property." },
	{ "client-cert", "Contains the client certificate if used by the EAP method specified in the \"eap\" property. Certificate data is specified using a \"scheme\"; two are currently supported: blob and path. When using the blob scheme (which is backwards compatible with NM 0.7.x) this property should be set to the certificate's DER encoded data. When using the path scheme, this property should be set to the full UTF-8 encoded path of the certificate, prefixed with the string \"file://\" and ending with a terminating NUL byte." },
	{ "eap", "The allowed EAP method to be used when authenticating to the network with 802.1x.  Valid methods are: \"leap\", \"md5\", \"tls\", \"peap\", \"ttls\", \"pwd\", and \"fast\".  Each method requires different configuration using the properties of this setting; refer to wpa_supplicant documentation for the allowed combinations." },
	{ "identity", "Identity string for EAP authentication methods.  Often the user's user or login name." },
	{ "name", "The setting's name, which uniquely identifies the setting within the connection.  Each setting type has a name unique to that type, for example \"ppp\" or \"wireless\" or \"wired\"." },
	{ "pac-file", "UTF-8 encoded file path containing PAC for EAP-FAST." },
	{ "password", "UTF-8 encoded password used for EAP authentication methods. If both the \"password\" property and the \"password-raw\" property are specified, \"password\" is preferred." },
	{ "password-flags", "Flags indicating how to handle the \"password\" property." },
	{ "password-raw", "Password used for EAP authentication methods, given as a byte array to allow passwords in other encodings than UTF-8 to be used. If both the \"password\" property and the \"password-raw\" property are specified, \"password\" is preferred." },
	{ "password-raw-flags", "Flags indicating how to handle the \"password-raw\" property." },
	{ "phase1-fast-provisioning", "Enables or disables in-line provisioning of EAP-FAST credentials when FAST is specified as the EAP method in the \"eap\" property. Recognized values are \"0\" (disabled), \"1\" (allow unauthenticated provisioning), \"2\" (allow authenticated provisioning), and \"3\" (allow both authenticated and unauthenticated provisioning).  See the wpa_supplicant documentation for more details." },
	{ "phase1-peaplabel", "Forces use of the new PEAP label during key derivation.  Some RADIUS servers may require forcing the new PEAP label to interoperate with PEAPv1.  Set to \"1\" to force use of the new PEAP label.  See the wpa_supplicant documentation for more details." },
	{ "phase1-peapver", "Forces which PEAP version is used when PEAP is set as the EAP method in the \"eap\" property.  When unset, the version reported by the server will be used.  Sometimes when using older RADIUS servers, it is necessary to force the client to use a particular PEAP version.  To do so, this property may be set to \"0\" or \"1\" to force that specific PEAP version." },
	{ "phase2-altsubject-matches", "List of strings to be matched against the altSubjectName of the certificate presented by the authentication server during the inner \"phase 2\" authentication. If the list is empty, no verification of the server certificate's altSubjectName is performed." },
	{ "phase2-auth", "Specifies the allowed \"phase 2\" inner non-EAP authentication methods when an EAP method that uses an inner TLS tunnel is specified in the \"eap\" property.  Recognized non-EAP \"phase 2\" methods are \"pap\", \"chap\", \"mschap\", \"mschapv2\", \"gtc\", \"otp\", \"md5\", and \"tls\". Each \"phase 2\" inner method requires specific parameters for successful authentication; see the wpa_supplicant documentation for more details." },
	{ "phase2-autheap", "Specifies the allowed \"phase 2\" inner EAP-based authentication methods when an EAP method that uses an inner TLS tunnel is specified in the \"eap\" property.  Recognized EAP-based \"phase 2\" methods are \"md5\", \"mschapv2\", \"otp\", \"gtc\", and \"tls\". Each \"phase 2\" inner method requires specific parameters for successful authentication; see the wpa_supplicant documentation for more details." },
	{ "phase2-ca-cert", "Contains the \"phase 2\" CA certificate if used by the EAP method specified in the \"phase2-auth\" or \"phase2-autheap\" properties. Certificate data is specified using a \"scheme\"; two are currently supported: blob and path. When using the blob scheme (which is backwards compatible with NM 0.7.x) this property should be set to the certificate's DER encoded data. When using the path scheme, this property should be set to the full UTF-8 encoded path of the certificate, prefixed with the string \"file://\" and ending with a terminating NUL byte. This property can be unset even if the EAP method supports CA certificates, but this allows man-in-the-middle attacks and is NOT recommended." },
	{ "phase2-ca-path", "UTF-8 encoded path to a directory containing PEM or DER formatted certificates to be added to the verification chain in addition to the certificate specified in the \"phase2-ca-cert\" property." },
	{ "phase2-client-cert", "Contains the \"phase 2\" client certificate if used by the EAP method specified in the \"phase2-auth\" or \"phase2-autheap\" properties. Certificate data is specified using a \"scheme\"; two are currently supported: blob and path. When using the blob scheme (which is backwards compatible with NM 0.7.x) this property should be set to the certificate's DER encoded data. When using the path scheme, this property should be set to the full UTF-8 encoded path of the certificate, prefixed with the string \"file://\" and ending with a terminating NUL byte. This property can be unset even if the EAP method supports CA certificates, but this allows man-in-the-middle attacks and is NOT recommended." },
	{ "phase2-private-key", "Contains the \"phase 2\" inner private key when the \"phase2-auth\" or \"phase2-autheap\" property is set to \"tls\". Key data is specified using a \"scheme\"; two are currently supported: blob and path. When using the blob scheme and private keys, this property should be set to the key's encrypted PEM encoded data. When using private keys with the path scheme, this property should be set to the full UTF-8 encoded path of the key, prefixed with the string \"file://\" and ending with a terminating NUL byte. When using PKCS#12 format private keys and the blob scheme, this property should be set to the PKCS#12 data and the \"phase2-private-key-password\" property must be set to password used to decrypt the PKCS#12 certificate and key. When using PKCS#12 files and the path scheme, this property should be set to the full UTF-8 encoded path of the key, prefixed with the string \"file://\" and and ending with a terminating NUL byte, and as with the blob scheme the \"phase2-private-key-password\" property must be set to the password used to decode the PKCS#12 private key and certificate." },
	{ "phase2-private-key-password", "The password used to decrypt the \"phase 2\" private key specified in the \"phase2-private-key\" property when the private key either uses the path scheme, or is a PKCS#12 format key." },
	{ "phase2-private-key-password-flags", "Flags indicating how to handle the \"phase2-private-key-password\" property." },
	{ "phase2-subject-match", "Substring to be matched against the subject of the certificate presented by the authentication server during the inner \"phase 2\" authentication. When unset, no verification of the authentication server certificate's subject is performed." },
	{ "pin", "PIN used for EAP authentication methods." },
	{ "pin-flags", "Flags indicating how to handle the \"pin\" property." },
	{ "private-key", "Contains the private key when the \"eap\" property is set to \"tls\". Key data is specified using a \"scheme\"; two are currently supported: blob and path. When using the blob scheme and private keys, this property should be set to the key's encrypted PEM encoded data. When using private keys with the path scheme, this property should be set to the full UTF-8 encoded path of the key, prefixed with the string \"file://\" and ending with a terminating NUL byte. When using PKCS#12 format private keys and the blob scheme, this property should be set to the PKCS#12 data and the \"private-key-password\" property must be set to password used to decrypt the PKCS#12 certificate and key. When using PKCS#12 files and the path scheme, this property should be set to the full UTF-8 encoded path of the key, prefixed with the string \"file://\" and and ending with a terminating NUL byte, and as with the blob scheme the \"private-key-password\" property must be set to the password used to decode the PKCS#12 private key and certificate. WARNING: \"private-key\" is not a \"secret\" property, and thus unencrypted private key data using the BLOB scheme may be readable by unprivileged users.  Private keys should always be encrypted with a private key password to prevent unauthorized access to unencrypted private key data." },
	{ "private-key-password", "The password used to decrypt the private key specified in the \"private-key\" property when the private key either uses the path scheme, or if the private key is a PKCS#12 format key." },
	{ "private-key-password-flags", "Flags indicating how to handle the \"private-key-password\" property." },
	{ "subject-match", "Substring to be matched against the subject of the certificate presented by the authentication server. When unset, no verification of the authentication server certificate's subject is performed." },
	{ "system-ca-certs", "When TRUE, overrides the \"ca-path\" and \"phase2-ca-path\" properties using the system CA directory specified at configure time with the --system-ca-path switch.  The certificates in this directory are added to the verification chain in addition to any certificates specified by the \"ca-cert\" and \"phase2-ca-cert\" properties. If the path provided with --system-ca-path is rather a file name (bundle of trusted CA certificates), it overrides \"ca-cert\" and \"phase2-ca-cert\" properties instead (sets ca_cert/ca_cert2 options for wpa_supplicant)." },
};
  
NmcPropertyDesc setting_802_3_ethernet[] = {
	{ "auto-negotiate", "If TRUE, allow auto-negotiation of port speed and duplex mode.  If FALSE, do not allow auto-negotiation, in which case the \"speed\" and \"duplex\" properties should be set." },
	{ "cloned-mac-address", "If specified, request that the device use this MAC address instead of its permanent MAC address.  This is known as MAC cloning or spoofing." },
	{ "duplex", "If specified, request that the device only use the specified duplex mode. Either \"half\" or \"full\"." },
	{ "mac-address", "If specified, this connection will only apply to the Ethernet device whose permanent MAC address matches. This property does not change the MAC address of the device (i.e. MAC spoofing)." },
	{ "mac-address-blacklist", "If specified, this connection will never apply to the Ethernet device whose permanent MAC address matches an address in the list.  Each MAC address is in the standard hex-digits-and-colons notation (00:11:22:33:44:55)." },
	{ "mtu", "If non-zero, only transmit packets of the specified size or smaller, breaking larger packets up into multiple Ethernet frames." },
	{ "name", "The setting's name, which uniquely identifies the setting within the connection.  Each setting type has a name unique to that type, for example \"ppp\" or \"wireless\" or \"wired\"." },
	{ "port", "Specific port type to use if multiple the device supports multiple attachment methods.  One of \"tp\" (Twisted Pair), \"aui\" (Attachment Unit Interface), \"bnc\" (Thin Ethernet) or \"mii\" (Media Independent Interface. If the device supports only one port type, this setting is ignored." },
	{ "s390-nettype", "s390 network device type; one of \"qeth\", \"lcs\", or \"ctc\", representing the different types of virtual network devices available on s390 systems." },
	{ "s390-options", "Dictionary of key/value pairs of s390-specific device options.  Both keys and values must be strings.  Allowed keys include \"portno\", \"layer2\", \"portname\", \"protocol\", among others.  Key names must contain only alphanumeric characters (ie, [a-zA-Z0-9])." },
	{ "s390-subchannels", "Identifies specific subchannels that this network device uses for communication with z/VM or s390 host.  Like the \"mac-address\" property for non-z/VM devices, this property can be used to ensure this connection only applies to the network device that uses these subchannels.  The list should contain exactly 3 strings, and each string may only be composed of hexadecimal characters and the period (.) character." },
	{ "speed", "If non-zero, request that the device use only the specified speed.  In Mbit/s, ie 100 == 100Mbit/s." },
};
  
NmcPropertyDesc setting_adsl[] = {
	{ "encapsulation", "Encapsulation of ADSL connection.  Can be \"vcmux\" or \"llc\"." },
	{ "name", "The setting's name, which uniquely identifies the setting within the connection.  Each setting type has a name unique to that type, for example \"ppp\" or \"wireless\" or \"wired\"." },
	{ "password", "Password used to authenticate with the ADSL service." },
	{ "password-flags", "Flags indicating how to handle the \"password\" property." },
	{ "protocol", "ADSL connection protocol.  Can be \"pppoa\", \"pppoe\" or \"ipoatm\"." },
	{ "username", "Username used to authenticate with the ADSL service." },
	{ "vci", "VCI of ADSL connection" },
	{ "vpi", "VPI of ADSL connection" },
};
  
NmcPropertyDesc setting_bluetooth[] = {
	{ "bdaddr", "The Bluetooth address of the device." },
	{ "name", "The setting's name, which uniquely identifies the setting within the connection.  Each setting type has a name unique to that type, for example \"ppp\" or \"wireless\" or \"wired\"." },
	{ "type", "Either \"dun\" for Dial-Up Networking connections or \"panu\" for Personal Area Networking connections to devices supporting the NAP profile." },
};
  
NmcPropertyDesc setting_bond[] = {
	{ "name", "The setting's name, which uniquely identifies the setting within the connection.  Each setting type has a name unique to that type, for example \"ppp\" or \"wireless\" or \"wired\"." },
	{ "options", "Dictionary of key/value pairs of bonding options.  Both keys and values must be strings. Option names must contain only alphanumeric characters (ie, [a-zA-Z0-9])." },
};
  
NmcPropertyDesc setting_bridge[] = {
	{ "ageing-time", "The Ethernet MAC address aging time, in seconds." },
	{ "forward-delay", "The Spanning Tree Protocol (STP) forwarding delay, in seconds." },
	{ "hello-time", "The Spanning Tree Protocol (STP) hello time, in seconds." },
	{ "mac-address", "If specified, the MAC address of bridge. When creating a new bridge, this MAC address will be set. When matching an existing (outside NetworkManager created) bridge, this MAC address must match." },
	{ "max-age", "The Spanning Tree Protocol (STP) maximum message age, in seconds." },
	{ "name", "The setting's name, which uniquely identifies the setting within the connection.  Each setting type has a name unique to that type, for example \"ppp\" or \"wireless\" or \"wired\"." },
	{ "priority", "Sets the Spanning Tree Protocol (STP) priority for this bridge.  Lower values are \"better\"; the lowest priority bridge will be elected the root bridge." },
	{ "stp", "Controls whether Spanning Tree Protocol (STP) is enabled for this bridge." },
};
  
NmcPropertyDesc setting_bridge_port[] = {
	{ "hairpin-mode", "Enables or disabled \"hairpin mode\" for the port, which allows frames to be sent back out through the port the frame was received on." },
	{ "name", "The setting's name, which uniquely identifies the setting within the connection.  Each setting type has a name unique to that type, for example \"ppp\" or \"wireless\" or \"wired\"." },
	{ "path-cost", "The Spanning Tree Protocol (STP) port cost for destinations via this port." },
	{ "priority", "The Spanning Tree Protocol (STP) priority of this bridge port." },
};
  
NmcPropertyDesc setting_cdma[] = {
	{ "name", "The setting's name, which uniquely identifies the setting within the connection.  Each setting type has a name unique to that type, for example \"ppp\" or \"wireless\" or \"wired\"." },
	{ "number", "The number to dial to establish the connection to the CDMA-based mobile broadband network, if any.  If not specified, the default number (#777) is used when required." },
	{ "password", "The password used to authenticate with the network, if required.  Many providers do not require a password, or accept any password.  But if a password is required, it is specified here." },
	{ "password-flags", "Flags indicating how to handle the \"password\" property." },
	{ "username", "The username used to authenticate with the network, if required.  Many providers do not require a username, or accept any username.  But if a username is required, it is specified here." },
};
  
NmcPropertyDesc setting_connection[] = {
	{ "autoconnect", "Whether or not the connection should be automatically connected by NetworkManager when the resources for the connection are available. TRUE to automatically activate the connection, FALSE to require manual intervention to activate the connection." },
	{ "autoconnect-priority", "The autoconnect priority. If the connection is set to autoconnect, connections with higher priority will be preferred. Defaults to 0. The higher number means higher priority." },
	{ "autoconnect-slaves", "Whether or not slaves of this connection should be automatically brought up when NetworkManager activates this connection. This only has a real effect for master connections. The permitted values are: 0: leave slave connections untouched, 1: activate all the slave connections with this connection, -1: default. If -1 (default) is set, global connection.autoconnect-slaves is read to determine the real value. If it is default as well, this fallbacks to 0." },
	{ "gateway-ping-timeout", "If greater than zero, delay success of IP addressing until either the timeout is reached, or an IP gateway replies to a ping." },
	{ "id", "A human readable unique identifier for the connection, like \"Work Wi-Fi\" or \"T-Mobile 3G\"." },
	{ "interface-name", "The name of the network interface this connection is bound to. If not set, then the connection can be attached to any interface of the appropriate type (subject to restrictions imposed by other settings). For software devices this specifies the name of the created device. For connection types where interface names cannot easily be made persistent (e.g. mobile broadband or USB Ethernet), this property should not be used. Setting this property restricts the interfaces a connection can be used with, and if interface names change or are reordered the connection may be applied to the wrong interface." },
	{ "master", "Interface name of the master device or UUID of the master connection." },
	{ "name", "The setting's name, which uniquely identifies the setting within the connection.  Each setting type has a name unique to that type, for example \"ppp\" or \"wireless\" or \"wired\"." },
	{ "permissions", "An array of strings defining what access a given user has to this connection.  If this is NULL or empty, all users are allowed to access this connection.  Otherwise a user is allowed to access this connection if and only if they are in this list. Each entry is of the form \"[type]:[id]:[reserved]\"; for example, \"user:dcbw:blah\". At this time only the \"user\" [type] is allowed.  Any other values are ignored and reserved for future use.  [id] is the username that this permission refers to, which may not contain the \":\" character. Any [reserved] information present must be ignored and is reserved for future use.  All of [type], [id], and [reserved] must be valid UTF-8." },
	{ "read-only", "FALSE if the connection can be modified using the provided settings service's D-Bus interface with the right privileges, or TRUE if the connection is read-only and cannot be modified." },
	{ "secondaries", "List of connection UUIDs that should be activated when the base connection itself is activated. Currently only VPN connections are supported." },
	{ "slave-type", "Setting name of the device type of this slave's master connection (eg, \"bond\"), or NULL if this connection is not a slave." },
	{ "timestamp", "The time, in seconds since the Unix Epoch, that the connection was last _successfully_ fully activated. NetworkManager updates the connection timestamp periodically when the connection is active to ensure that an active connection has the latest timestamp. The property is only meant for reading (changes to this property will not be preserved)." },
	{ "type", "Base type of the connection. For hardware-dependent connections, should contain the setting name of the hardware-type specific setting (ie, \"802-3-ethernet\" or \"802-11-wireless\" or \"bluetooth\", etc), and for non-hardware dependent connections like VPN or otherwise, should contain the setting name of that setting type (ie, \"vpn\" or \"bridge\", etc)." },
	{ "uuid", "A universally unique identifier for the connection, for example generated with libuuid.  It should be assigned when the connection is created, and never changed as long as the connection still applies to the same network.  For example, it should not be changed when the \"id\" property or NMSettingIP4Config changes, but might need to be re-created when the Wi-Fi SSID, mobile broadband network provider, or \"type\" property changes. The UUID must be in the format \"2815492f-7e56-435e-b2e9-246bd7cdc664\" (ie, contains only hexadecimal characters and \"-\")." },
	{ "zone", "The trust level of a the connection.  Free form case-insensitive string (for example \"Home\", \"Work\", \"Public\").  NULL or unspecified zone means the connection will be placed in the default zone as defined by the firewall." },
};
  
NmcPropertyDesc setting_dcb[] = {
	{ "app-fcoe-flags", "Specifies the NMSettingDcbFlags for the DCB FCoE application.  Flags may be any combination of NM_SETTING_DCB_FLAG_ENABLE (0x1), NM_SETTING_DCB_FLAG_ADVERTISE (0x2), and NM_SETTING_DCB_FLAG_WILLING (0x4)." },
	{ "app-fcoe-mode", "The FCoE controller mode; either \"fabric\" (default) or \"vn2vn\"." },
	{ "app-fcoe-priority", "The highest User Priority (0 - 7) which FCoE frames should use, or -1 for default priority.  Only used when the \"app-fcoe-flags\" property includes the NM_SETTING_DCB_FLAG_ENABLE (0x1) flag." },
	{ "app-fip-flags", "Specifies the NMSettingDcbFlags for the DCB FIP application.  Flags may be any combination of NM_SETTING_DCB_FLAG_ENABLE (0x1), NM_SETTING_DCB_FLAG_ADVERTISE (0x2), and NM_SETTING_DCB_FLAG_WILLING (0x4)." },
	{ "app-fip-priority", "The highest User Priority (0 - 7) which FIP frames should use, or -1 for default priority.  Only used when the \"app-fip-flags\" property includes the NM_SETTING_DCB_FLAG_ENABLE (0x1) flag." },
	{ "app-iscsi-flags", "Specifies the NMSettingDcbFlags for the DCB iSCSI application.  Flags may be any combination of NM_SETTING_DCB_FLAG_ENABLE (0x1), NM_SETTING_DCB_FLAG_ADVERTISE (0x2), and NM_SETTING_DCB_FLAG_WILLING (0x4)." },
	{ "app-iscsi-priority", "The highest User Priority (0 - 7) which iSCSI frames should use, or -1 for default priority. Only used when the \"app-iscsi-flags\" property includes the NM_SETTING_DCB_FLAG_ENABLE (0x1) flag." },
	{ "name", "The setting's name, which uniquely identifies the setting within the connection.  Each setting type has a name unique to that type, for example \"ppp\" or \"wireless\" or \"wired\"." },
	{ "priority-bandwidth", "An array of 8 uint values, where the array index corresponds to the User Priority (0 - 7) and the value indicates the percentage of bandwidth of the priority's assigned group that the priority may use.  The sum of all percentages for priorities which belong to the same group must total 100 percent." },
	{ "priority-flow-control", "An array of 8 boolean values, where the array index corresponds to the User Priority (0 - 7) and the value indicates whether or not the corresponding priority should transmit priority pause." },
	{ "priority-flow-control-flags", "Specifies the NMSettingDcbFlags for DCB Priority Flow Control (PFC). Flags may be any combination of NM_SETTING_DCB_FLAG_ENABLE (0x1), NM_SETTING_DCB_FLAG_ADVERTISE (0x2), and NM_SETTING_DCB_FLAG_WILLING (0x4)." },
	{ "priority-group-bandwidth", "An array of 8 uint values, where the array index corresponds to the Priority Group ID (0 - 7) and the value indicates the percentage of link bandwidth allocated to that group.  Allowed values are 0 - 100, and the sum of all values must total 100 percent." },
	{ "priority-group-flags", "Specifies the NMSettingDcbFlags for DCB Priority Groups.  Flags may be any combination of NM_SETTING_DCB_FLAG_ENABLE (0x1), NM_SETTING_DCB_FLAG_ADVERTISE (0x2), and NM_SETTING_DCB_FLAG_WILLING (0x4)." },
	{ "priority-group-id", "An array of 8 uint values, where the array index corresponds to the User Priority (0 - 7) and the value indicates the Priority Group ID.  Allowed Priority Group ID values are 0 - 7 or 15 for the unrestricted group." },
	{ "priority-strict-bandwidth", "An array of 8 boolean values, where the array index corresponds to the User Priority (0 - 7) and the value indicates whether or not the priority may use all of the bandwidth allocated to its assigned group." },
	{ "priority-traffic-class", "An array of 8 uint values, where the array index corresponds to the User Priority (0 - 7) and the value indicates the traffic class (0 - 7) to which the priority is mapped." },
};
  
NmcPropertyDesc setting_generic[] = {
	{ "name", "The setting's name, which uniquely identifies the setting within the connection.  Each setting type has a name unique to that type, for example \"ppp\" or \"wireless\" or \"wired\"." },
};
  
NmcPropertyDesc setting_gsm[] = {
	{ "apn", "The GPRS Access Point Name specifying the APN used when establishing a data session with the GSM-based network.  The APN often determines how the user will be billed for their network usage and whether the user has access to the Internet or just a provider-specific walled-garden, so it is important to use the correct APN for the user's mobile broadband plan. The APN may only be composed of the characters a-z, 0-9, ., and - per GSM 03.60 Section 14.9." },
	{ "home-only", "When TRUE, only connections to the home network will be allowed. Connections to roaming networks will not be made." },
	{ "name", "The setting's name, which uniquely identifies the setting within the connection.  Each setting type has a name unique to that type, for example \"ppp\" or \"wireless\" or \"wired\"." },
	{ "network-id", "The Network ID (GSM LAI format, ie MCC-MNC) to force specific network registration.  If the Network ID is specified, NetworkManager will attempt to force the device to register only on the specified network. This can be used to ensure that the device does not roam when direct roaming control of the device is not otherwise possible." },
	{ "number", "Number to dial when establishing a PPP data session with the GSM-based mobile broadband network.  Many modems do not require PPP for connections to the mobile network and thus this property should be left blank, which allows NetworkManager to select the appropriate settings automatically." },
	{ "password", "The password used to authenticate with the network, if required.  Many providers do not require a password, or accept any password.  But if a password is required, it is specified here." },
	{ "password-flags", "Flags indicating how to handle the \"password\" property." },
	{ "pin", "If the SIM is locked with a PIN it must be unlocked before any other operations are requested.  Specify the PIN here to allow operation of the device." },
	{ "pin-flags", "Flags indicating how to handle the \"pin\" property." },
	{ "username", "The username used to authenticate with the network, if required.  Many providers do not require a username, or accept any username.  But if a username is required, it is specified here." },
};
  
NmcPropertyDesc setting_infiniband[] = {
	{ "mac-address", "If specified, this connection will only apply to the IPoIB device whose permanent MAC address matches. This property does not change the MAC address of the device (i.e. MAC spoofing)." },
	{ "mtu", "If non-zero, only transmit packets of the specified size or smaller, breaking larger packets up into multiple frames." },
	{ "name", "The setting's name, which uniquely identifies the setting within the connection.  Each setting type has a name unique to that type, for example \"ppp\" or \"wireless\" or \"wired\"." },
	{ "p-key", "The InfiniBand P_Key to use for this device. A value of -1 means to use the default P_Key (aka \"the P_Key at index 0\").  Otherwise it is a 16-bit unsigned integer, whose high bit is set if it is a \"full membership\" P_Key." },
	{ "parent", "The interface name of the parent device of this device. Normally NULL, but if the \"p_key\" property is set, then you must specify the base device by setting either this property or \"mac-address\"." },
	{ "transport-mode", "The IP-over-InfiniBand transport mode. Either \"datagram\" or \"connected\"." },
};
  
NmcPropertyDesc setting_ipv4[] = {
	{ "addresses", "Array of IP addresses." },
	{ "dhcp-client-id", "A string sent to the DHCP server to identify the local machine which the DHCP server may use to customize the DHCP lease and options." },
	{ "dhcp-hostname", "If the \"dhcp-send-hostname\" property is TRUE, then the specified name will be sent to the DHCP server when acquiring a lease." },
	{ "dhcp-send-hostname", "If TRUE, a hostname is sent to the DHCP server when acquiring a lease. Some DHCP servers use this hostname to update DNS databases, essentially providing a static hostname for the computer.  If the \"dhcp-hostname\" property is NULL and this property is TRUE, the current persistent hostname of the computer is sent." },
	{ "dns", "Array of IP addresses of DNS servers." },
	{ "dns-search", "Array of DNS search domains." },
	{ "gateway", "The gateway associated with this configuration. This is only meaningful if \"addresses\" is also set." },
	{ "ignore-auto-dns", "When \"method\" is set to \"auto\" and this property to TRUE, automatically configured nameservers and search domains are ignored and only nameservers and search domains specified in the \"dns\" and \"dns-search\" properties, if any, are used." },
	{ "ignore-auto-routes", "When \"method\" is set to \"auto\" and this property to TRUE, automatically configured routes are ignored and only routes specified in the \"routes\" property, if any, are used." },
	{ "may-fail", "If TRUE, allow overall network configuration to proceed even if the configuration specified by this property times out.  Note that at least one IP configuration must succeed or overall network configuration will still fail.  For example, in IPv6-only networks, setting this property to TRUE on the NMSettingIP4Config allows the overall network configuration to succeed if IPv4 configuration fails but IPv6 configuration completes successfully." },
	{ "method", "IP configuration method. NMSettingIP4Config and NMSettingIP6Config both support \"auto\", \"manual\", and \"link-local\". See the subclass-specific documentation for other values. In general, for the \"auto\" method, properties such as \"dns\" and \"routes\" specify information that is added on to the information returned from automatic configuration.  The \"ignore-auto-routes\" and \"ignore-auto-dns\" properties modify this behavior. For methods that imply no upstream network, such as \"shared\" or \"link-local\", these properties must be empty." },
	{ "name", "The setting's name, which uniquely identifies the setting within the connection.  Each setting type has a name unique to that type, for example \"ppp\" or \"wireless\" or \"wired\"." },
	{ "never-default", "If TRUE, this connection will never be the default connection for this IP type, meaning it will never be assigned the default route by NetworkManager." },
	{ "route-metric", "The default metric for routes that don't explicitly specify a metric. The default value -1 means that the metric is choosen automatically based on the device type. The metric applies to dynamic routes, manual (static) routes that don't have an explicit metric setting, address prefix routes, and the default route. Note that for IPv6, the kernel accepts zero (0) but coerces it to 1024 (user default). Hence, setting this property to zero effectively mean setting it to 1024. For IPv4, zero is a regular value for the metric." },
	{ "routes", "Array of IP routes." },
};
  
NmcPropertyDesc setting_ipv6[] = {
	{ "addresses", "Array of IP addresses." },
	{ "dhcp-hostname", "If the \"dhcp-send-hostname\" property is TRUE, then the specified name will be sent to the DHCP server when acquiring a lease." },
	{ "dhcp-send-hostname", "If TRUE, a hostname is sent to the DHCP server when acquiring a lease. Some DHCP servers use this hostname to update DNS databases, essentially providing a static hostname for the computer.  If the \"dhcp-hostname\" property is NULL and this property is TRUE, the current persistent hostname of the computer is sent." },
	{ "dns", "Array of IP addresses of DNS servers." },
	{ "dns-search", "Array of DNS search domains." },
	{ "gateway", "The gateway associated with this configuration. This is only meaningful if \"addresses\" is also set." },
	{ "ignore-auto-dns", "When \"method\" is set to \"auto\" and this property to TRUE, automatically configured nameservers and search domains are ignored and only nameservers and search domains specified in the \"dns\" and \"dns-search\" properties, if any, are used." },
	{ "ignore-auto-routes", "When \"method\" is set to \"auto\" and this property to TRUE, automatically configured routes are ignored and only routes specified in the \"routes\" property, if any, are used." },
	{ "ip6-privacy", "Configure IPv6 Privacy Extensions for SLAAC, described in RFC4941.  If enabled, it makes the kernel generate a temporary IPv6 address in addition to the public one generated from MAC address via modified EUI-64.  This enhances privacy, but could cause problems in some applications, on the other hand.  The permitted values are: -1: unknown, 0: disabled, 1: enabled (prefer public address), 2: enabled (prefer temporary addresses). Having a per-connection setting set to \"-1\" (unknown) means fallback to global configuration \"ipv6.ip6-privacy\". If also global configuration is unspecified or set to \"-1\", fallback to read \"/proc/sys/net/ipv6/conf/default/use_tempaddr\"." },
	{ "may-fail", "If TRUE, allow overall network configuration to proceed even if the configuration specified by this property times out.  Note that at least one IP configuration must succeed or overall network configuration will still fail.  For example, in IPv6-only networks, setting this property to TRUE on the NMSettingIP4Config allows the overall network configuration to succeed if IPv4 configuration fails but IPv6 configuration completes successfully." },
	{ "method", "IP configuration method. NMSettingIP4Config and NMSettingIP6Config both support \"auto\", \"manual\", and \"link-local\". See the subclass-specific documentation for other values. In general, for the \"auto\" method, properties such as \"dns\" and \"routes\" specify information that is added on to the information returned from automatic configuration.  The \"ignore-auto-routes\" and \"ignore-auto-dns\" properties modify this behavior. For methods that imply no upstream network, such as \"shared\" or \"link-local\", these properties must be empty." },
	{ "name", "The setting's name, which uniquely identifies the setting within the connection.  Each setting type has a name unique to that type, for example \"ppp\" or \"wireless\" or \"wired\"." },
	{ "never-default", "If TRUE, this connection will never be the default connection for this IP type, meaning it will never be assigned the default route by NetworkManager." },
	{ "route-metric", "The default metric for routes that don't explicitly specify a metric. The default value -1 means that the metric is choosen automatically based on the device type. The metric applies to dynamic routes, manual (static) routes that don't have an explicit metric setting, address prefix routes, and the default route. Note that for IPv6, the kernel accepts zero (0) but coerces it to 1024 (user default). Hence, setting this property to zero effectively mean setting it to 1024. For IPv4, zero is a regular value for the metric." },
	{ "routes", "Array of IP routes." },
};
  
NmcPropertyDesc setting_ppp[] = {
	{ "baud", "If non-zero, instruct pppd to set the serial port to the specified baudrate.  This value should normally be left as 0 to automatically choose the speed." },
	{ "crtscts", "If TRUE, specify that pppd should set the serial port to use hardware flow control with RTS and CTS signals.  This value should normally be set to FALSE." },
	{ "lcp-echo-failure", "If non-zero, instruct pppd to presume the connection to the peer has failed if the specified number of LCP echo-requests go unanswered by the peer.  The \"lcp-echo-interval\" property must also be set to a non-zero value if this property is used." },
	{ "lcp-echo-interval", "If non-zero, instruct pppd to send an LCP echo-request frame to the peer every n seconds (where n is the specified value).  Note that some PPP peers will respond to echo requests and some will not, and it is not possible to autodetect this." },
	{ "mppe-stateful", "If TRUE, stateful MPPE is used.  See pppd documentation for more information on stateful MPPE." },
	{ "mru", "If non-zero, instruct pppd to request that the peer send packets no larger than the specified size.  If non-zero, the MRU should be between 128 and 16384." },
	{ "mtu", "If non-zero, instruct pppd to send packets no larger than the specified size." },
	{ "name", "The setting's name, which uniquely identifies the setting within the connection.  Each setting type has a name unique to that type, for example \"ppp\" or \"wireless\" or \"wired\"." },
	{ "no-vj-comp", "If TRUE, Van Jacobsen TCP header compression will not be requested." },
	{ "noauth", "If TRUE, do not require the other side (usually the PPP server) to authenticate itself to the client.  If FALSE, require authentication from the remote side.  In almost all cases, this should be TRUE." },
	{ "nobsdcomp", "If TRUE, BSD compression will not be requested." },
	{ "nodeflate", "If TRUE, \"deflate\" compression will not be requested." },
	{ "refuse-chap", "If TRUE, the CHAP authentication method will not be used." },
	{ "refuse-eap", "If TRUE, the EAP authentication method will not be used." },
	{ "refuse-mschap", "If TRUE, the MSCHAP authentication method will not be used." },
	{ "refuse-mschapv2", "If TRUE, the MSCHAPv2 authentication method will not be used." },
	{ "refuse-pap", "If TRUE, the PAP authentication method will not be used." },
	{ "require-mppe", "If TRUE, MPPE (Microsoft Point-to-Point Encrpytion) will be required for the PPP session.  If either 64-bit or 128-bit MPPE is not available the session will fail.  Note that MPPE is not used on mobile broadband connections." },
	{ "require-mppe-128", "If TRUE, 128-bit MPPE (Microsoft Point-to-Point Encrpytion) will be required for the PPP session, and the \"require-mppe\" property must also be set to TRUE.  If 128-bit MPPE is not available the session will fail." },
};
  
NmcPropertyDesc setting_pppoe[] = {
	{ "name", "The setting's name, which uniquely identifies the setting within the connection.  Each setting type has a name unique to that type, for example \"ppp\" or \"wireless\" or \"wired\"." },
	{ "password", "Password used to authenticate with the PPPoE service." },
	{ "password-flags", "Flags indicating how to handle the \"password\" property." },
	{ "service", "If specified, instruct PPPoE to only initiate sessions with access concentrators that provide the specified service.  For most providers, this should be left blank.  It is only required if there are multiple access concentrators or a specific service is known to be required." },
	{ "username", "Username used to authenticate with the PPPoE service." },
};
  
NmcPropertyDesc setting_serial[] = {
	{ "baud", "Speed to use for communication over the serial port.  Note that this value usually has no effect for mobile broadband modems as they generally ignore speed settings and use the highest available speed." },
	{ "bits", "Byte-width of the serial communication. The 8 in \"8n1\" for example." },
	{ "name", "The setting's name, which uniquely identifies the setting within the connection.  Each setting type has a name unique to that type, for example \"ppp\" or \"wireless\" or \"wired\"." },
	{ "parity", "Parity setting of the serial port." },
	{ "send-delay", "Time to delay between each byte sent to the modem, in microseconds." },
	{ "stopbits", "Number of stop bits for communication on the serial port.  Either 1 or 2. The 1 in \"8n1\" for example." },
};
  
NmcPropertyDesc setting_team[] = {
	{ "config", "The JSON configuration for the team network interface.  The property should contain raw JSON configuration data suitable for teamd, because the value is passed directly to teamd. If not specified, the default configuration is used.  See man teamd.conf for the format details." },
	{ "name", "The setting's name, which uniquely identifies the setting within the connection.  Each setting type has a name unique to that type, for example \"ppp\" or \"wireless\" or \"wired\"." },
};
  
NmcPropertyDesc setting_team_port[] = {
	{ "config", "The JSON configuration for the team port. The property should contain raw JSON configuration data suitable for teamd, because the value is passed directly to teamd. If not specified, the default configuration is used. See man teamd.conf for the format details." },
	{ "name", "The setting's name, which uniquely identifies the setting within the connection.  Each setting type has a name unique to that type, for example \"ppp\" or \"wireless\" or \"wired\"." },
};
  
NmcPropertyDesc setting_vlan[] = {
	{ "egress-priority-map", "For outgoing packets, a list of mappings from Linux SKB priorities to 802.1p priorities.  The mapping is given in the format \"from:to\" where both \"from\" and \"to\" are unsigned integers, ie \"7:3\"." },
	{ "flags", "One or more flags which control the behavior and features of the VLAN interface.  Flags include NM_VLAN_FLAG_REORDER_HEADERS (0x1) (reordering of output packet headers), NM_VLAN_FLAG_GVRP (0x2) (use of the GVRP protocol), and NM_VLAN_FLAG_LOOSE_BINDING (0x4) (loose binding of the interface to its master device's operating state)." },
	{ "id", "The VLAN identifier that the interface created by this connection should be assigned." },
	{ "ingress-priority-map", "For incoming packets, a list of mappings from 802.1p priorities to Linux SKB priorities.  The mapping is given in the format \"from:to\" where both \"from\" and \"to\" are unsigned integers, ie \"7:3\"." },
	{ "name", "The setting's name, which uniquely identifies the setting within the connection.  Each setting type has a name unique to that type, for example \"ppp\" or \"wireless\" or \"wired\"." },
	{ "parent", "If given, specifies the parent interface name or parent connection UUID from which this VLAN interface should be created.  If this property is not specified, the connection must contain an \"802-3-ethernet\" setting with a \"mac-address\" property." },
};
  
NmcPropertyDesc setting_vpn[] = {
	{ "data", "Dictionary of key/value pairs of VPN plugin specific data.  Both keys and values must be strings." },
	{ "name", "The setting's name, which uniquely identifies the setting within the connection.  Each setting type has a name unique to that type, for example \"ppp\" or \"wireless\" or \"wired\"." },
	{ "persistent", "If the VPN service supports persistence, and this property is TRUE, the VPN will attempt to stay connected across link changes and outages, until explicitly disconnected." },
	{ "secrets", "Dictionary of key/value pairs of VPN plugin specific secrets like passwords or private keys.  Both keys and values must be strings." },
	{ "service-type", "D-Bus service name of the VPN plugin that this setting uses to connect to its network.  i.e. org.freedesktop.NetworkManager.vpnc for the vpnc plugin." },
	{ "user-name", "If the VPN connection requires a user name for authentication, that name should be provided here.  If the connection is available to more than one user, and the VPN requires each user to supply a different name, then leave this property empty.  If this property is empty, NetworkManager will automatically supply the username of the user which requested the VPN connection." },
};
  
NmcPropertyDesc setting_wimax[] = {
	{ "mac-address", "If specified, this connection will only apply to the WiMAX device whose MAC address matches. This property does not change the MAC address of the device (known as MAC spoofing)." },
	{ "name", "The setting's name, which uniquely identifies the setting within the connection.  Each setting type has a name unique to that type, for example \"ppp\" or \"wireless\" or \"wired\"." },
	{ "network-name", "Network Service Provider (NSP) name of the WiMAX network this connection should use." },
};
  

typedef struct {
	const char *name;
	NmcPropertyDesc *properties;
	int n_properties;
} NmcSettingDesc;

NmcSettingDesc all_settings[] = {

	{ "802-11-olpc-mesh", setting_802_11_olpc_mesh, 4 },
	{ "802-11-wireless", setting_802_11_wireless, 14 },
	{ "802-11-wireless-security", setting_802_11_wireless_security, 18 },
	{ "802-1x", setting_802_1x, 33 },
	{ "802-3-ethernet", setting_802_3_ethernet, 12 },
	{ "adsl", setting_adsl, 8 },
	{ "bluetooth", setting_bluetooth, 3 },
	{ "bond", setting_bond, 2 },
	{ "bridge", setting_bridge, 8 },
	{ "bridge-port", setting_bridge_port, 4 },
	{ "cdma", setting_cdma, 5 },
	{ "connection", setting_connection, 16 },
	{ "dcb", setting_dcb, 16 },
	{ "generic", setting_generic, 1 },
	{ "gsm", setting_gsm, 10 },
	{ "infiniband", setting_infiniband, 6 },
	{ "ipv4", setting_ipv4, 15 },
	{ "ipv6", setting_ipv6, 15 },
	{ "ppp", setting_ppp, 19 },
	{ "pppoe", setting_pppoe, 5 },
	{ "serial", setting_serial, 6 },
	{ "team", setting_team, 2 },
	{ "team-port", setting_team_port, 2 },
	{ "vlan", setting_vlan, 6 },
	{ "vpn", setting_vpn, 6 },
	{ "wimax", setting_wimax, 3 },
};

static int
find_by_name (gconstpointer keyv, gconstpointer cmpv)
{
	const char *key = keyv;
	struct { const char *name; gpointer data; } *cmp = (gpointer)cmpv;

	return strcmp (key, cmp->name);
}

static const char *
nmc_setting_get_property_doc (NMSetting *setting, const char *prop)
{
	NmcSettingDesc *setting_desc;
	NmcPropertyDesc *property_desc;

	setting_desc = bsearch (nm_setting_get_name (setting),
	                        all_settings, G_N_ELEMENTS (all_settings),
	                        sizeof (NmcSettingDesc), find_by_name);
	if (!setting_desc)
		return NULL;
	property_desc = bsearch (prop,
	                         setting_desc->properties, setting_desc->n_properties,
	                         sizeof (NmcPropertyDesc), find_by_name);
	if (!property_desc)
		return NULL;
	return property_desc->docs;
}
  