// status can be "online", "idle", "dnd", or "invisible" or "offline"
import 'dotenv/config';
export default [
    {
        channelId: "1566253435051839498",
        serverId: "1496375885400506378",
        token: process.env.TOKEN1,
        selfDeaf: false,
        autoReconnect: {
            enabled: true,
            delay: 5, // ثواني
            maxRetries: 5,
        },
        presence: {
            status: "idle",
        },
        selfMute: true,
    },
];
