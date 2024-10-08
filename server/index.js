const express = require("express");
const app = express();

const http = require("http");
const cors = require("cors");

const { Server } = require("socket.io");
const { env } = require("process");

app.use(cors());

const server = http.createServer(app);

const PORT = process.env.PORT || 5173;

// create instance of the socket io server
const io = new Server(server, {
	cors: {
		origin: `http://localhost:${PORT}`,
		credentials: true,
		methods: ["GET", "POST"],
	},
});

// constantly listening
io.on("connection", (socket) => {
	console.log(`User Connected: ${socket.id}`);
	socket.on("screenshot", (data) => {
		console.log("Received screenshot event with data:", data);
		socket.broadcast.emit("screenshot", data);
	});
});

server.listen(3000, () => {
	console.log("SERVER IS RUNNING!");
});
