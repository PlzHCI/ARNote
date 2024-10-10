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
		origin: `http://10.131.100.68:${PORT}`,
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
	socket.on("ideation", (data) => {
		console.log("Received generate ideation event with data:", data);
		socket.broadcast.emit("ideation", data);
	});
	socket.on("result", (data) => {
		console.log("Received ideation result with data:", data);
		const stringData = JSON.stringify(data);
		socket.broadcast.emit("result", stringData);
		console.log("stringData", stringData);
	});
});

server.listen(3000, () => {
	console.log("SERVER IS RUNNING!");
});
