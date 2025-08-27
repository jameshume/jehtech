<style>
    pre > code {
        border: 0;
        background-color: inherit;
        font-size: 90%;
    }
</style>

## Integrate LwIP With Custom Ethernet NIC Driver
The core TCP/IP stack is hardware-independent. The only part that needs to be adapted for a new hardware platform is the network interface layer, which sits between the LwIP stack and the physical Ethernet hardware driver.

See `lwip/src/netif/ethernetif.c` for a skeleton for developing Ethernet network interface drivers for lwIP.

To add an interface:

```C
struct netif my_nif;
struct my_net_driver_context my_ctx;

...

static err_t my_nif_init(struct netif* nif) {
    nif->name[...] = ...;         // Set or copy a string here.
    nif->output = etharp_output;  // Called by IP module to send a packet on the interface, usually etharp_output().
                                  // etharp_output() resolves and fills-in the Ethernet address header for the 
                                  // outgoing IP packet. It is a function provided by LwIP. It will eventually call,
                                  // via ethernet_output(), nif->linkoutput() (see below).
    nif->linkoutput = nif_output; // Called by ethernet_output() to send a packet on the interface. Buffer output as is.
                                  // *** This is how we link the transmit side of a custom driver into LwIP ***
    nif->flags |= NETIF_FLAG_BROADCAST | NETIF_FLAG_ETHARP | ...;
    nif->mtu = ...;
    nif->hostname = ...;
    nif->hwaddr = .. set MAC ...;

    return ERR_OK;
}

// `ethernet_input` is a callback function that is called to pass ingress packets up the stack.
// I think this is now out of date.
// *** This is how we link the receive side of a custom driver into LwIP BUT I think its a little
//     wierd because LwIP doesn't actually call it. Our driver calls it! This just sets 
//     my_nif->input for us. ***
// 
//
if (netif_add_noaddr(&my_nif, &my_ctx, nif_init, ethernet_input  ) == NULL) {
    ... ERROR ...
}

// Newer version set it to tcpip_input()
```

## Custom Debug Output

In `lwipopts.h`:

```C
#define LWIP_DEBUG 1
#define ETHARP_DEBUG       LWIP_DBG_ON
#define NETIF_DEBUG        LWIP_DBG_ON
#define PBUF_DEBUG         LWIP_DBG_ON
#define SOCKETS_DEBUG      LWIP_DBG_ON
#define ICMP_DEBUG         LWIP_DBG_ON
#define IGMP_DEBUG         LWIP_DBG_ON
#define TCPIP_DEBUG        LWIP_DBG_ON
#define TCP_DEBUG          LWIP_DBG_ON
#define LWIP_DBG_MIN_LEVEL LWIP_DBG_LEVEL_WARNING 
extern void my_debug_printf_function(const char*fmt, ...);
#define LWIP_PLATFORM_DIAG(x) do {my_debug_printf_function x;} while(0)
```
