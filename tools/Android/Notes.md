### Typical security queries:

• Exported components → intent filters, deep links (you started this)
• Hardcoded secrets → string search in dx
• Crypto misuse → find SecretKeySpec, MessageDigest, weak modes
• WebView issues → addJavascriptInterface, setJavaScriptEnabled
• IPC → Binder, AIDL, ContentProvider URIs


### Quick reference

Permissions in AndroidManifest.xml  | a.get_permissions()
Human-readable permission details  | a.get_details_permissions()
Pretty-print APK summary  | a.show()
Which code paths likely need a permission | dx.get_permissions(apilevel)
Where a specific permission is used  | dx.get_permission_usage(perm, apilevel)