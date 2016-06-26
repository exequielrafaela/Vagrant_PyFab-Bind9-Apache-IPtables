;
; BIND data file for local loopback interface
;
$TTL	604800
@	IN	SOA	ns1.practico-integrador.com. admin.practico-integrador.com. (
			      3		; Serial
			 604800		; Refresh
			  86400		; Retry
			2419200		; Expire
			 604800 )	; Negative Cache TTL
;
;@	IN	NS	localhost.
;@	IN	A	127.0.0.1
;@	IN	AAAA	::1
;name servers - NS records
	IN	NS	ns1.practico-integrador.com.
	IN 	NS	ns2.practico-integrador.com.

; name servers - A records
ns1.practico-integrador.com.	IN	A	192.168.1.1
ns1.practico-integrador.com.	IN	A	192.168.3.2
ns2.practico-integrador.com.	IN 	A	172.16.2.1
