import * as React from "react";
import { useState, useEffect } from "react";
import { BarChart } from "@mui/x-charts/BarChart";
import { useCombinedContext } from "./context"; // Import the context hook
// import { useNavigate } from "react-router-dom";

export function Chart() {
    const { playersList} = useCombinedContext(); // Access playersList from the context
    const { teamsList } = useCombinedContext(); // Access teamsList from the context
    const [loading, setLoading] = useState(true);
    // const navigate = useNavigate();

    useEffect(() => {
        setLoading(false); // Set loading to false initially
        // Fetch data or set up websocket connection if needed
    }, []);

    const countPlayersByClub = (players) => {
        const clubs = {};
        players.forEach((player) => {
            if (clubs[player.team_id]) {
                clubs[player.team_id] += 1;
            } else {
                clubs[player.team_id] = 1;
            }
        });
        return clubs;
    };

    let barChartData = countPlayersByClub(playersList);
    barChartData = Object.keys(barChartData).map((team_id) => {
        // const team = teamsList.find((team) => team.id === idd);
        // const team_name = team ? team.name : 'Unknown';
        return {
            team_id: team_id,
            count: barChartData[team_id],
        };
    });

    const customTickFormatter = (value) => {
        const maxLength = 10;
        if (value.length > maxLength) {
            return value.substring(0, maxLength - 3) + '...';
        }
        return value;
    };

    const yTickFormatter = (value) => {
        return Math.round(value);
    };

    if (loading) {
        return <div>Loading...</div>;
    }

    return (
        <div>
            <h2>Bar Chart</h2>
            <BarChart 
                dataset={barChartData}
                xAxis={[{ scaleType: 'band', dataKey: 'team_id', tickFormater: customTickFormatter }]}
                series={[{ scaleType: 'band', dataKey: 'count' }]}
                width={1000}
                height={400}
            />
        </div>
    );
}
