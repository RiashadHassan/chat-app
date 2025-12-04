import { useState, useEffect } from "react";
import "./servers.css";

const ServersPage = () => {
  const [servers, setServers] = useState([]);

  const getServers = async () => {
    const url = "http://localhost/api/v1/servers/";
    try {
      const response = await fetch(url, {
        method: "GET",
        headers: { "Content-Type": "application/json" },
      });

      if (!response.ok) {
        console.error("Fetch error:", response.status);
        return;
      }

      const data = await response.json();
      console.log("DATA", data)
      setServers(data.results); // <-- store in state
    } catch (error) {
      console.error("Error fetching servers:", error);
    }
  };

  useEffect(() => {
    getServers();
  }, []);

const getServerInitials = (fullName) =>{
    const separatedList = fullName.split("-");    
    
    console.log(separatedList)
    const initialsList = separatedList.map((e)=>e[0])
    return initialsList.join("").toUpperCase()
};

  return (
    <div className="servers-layout">
      {/* LEFT SIDEBAR: SERVER ICONS */}
      <aside className="server-sidebar">
        <div className="server-icon home">H</div>

        {servers.map((server) => (
          <div key={server.uid} className="server-icon">
            {getServerInitials(server.name)}
          </div>
        ))}

        <div className="server-icon add">+</div>
      </aside>

      {/* MIDDLE SIDEBAR: CHANNEL LIST */}
      <aside className="channel-sidebar">
        <h2>Channels</h2>
        <ul>
          <li># general</li>
          <li># random</li>
          <li># announcements</li>
        </ul>
      </aside>

      {/* MAIN CONTENT */}
      <main className="main-content">
        <h1>Welcome!</h1>
        <p>Select a server or channel from the sidebar.</p>
      </main>
    </div>
  );
};

export default ServersPage;
