import * as React from "react";
import { useState, useEffect } from "react";
import { BarChart } from "@mui/x-charts/BarChart";

export function Chart() {
    const [players, setPlayers] = useState([]);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        fetch('http://127.0.0.1:8000/players')
            .then((response) => {
                if (!response.ok) {
                    throw new Error('Failed to fetch players');
                }
                return response.json();
            })
            .then((data) => {
                setPlayers(data);
                setLoading(false);
            })
            .catch((error) => {
                console.error('Error fetching players:', error);
                setLoading(false);
            });
    }, []);

    const countPlayersByClub = (players) => {
        const clubs = {};
        players.forEach((player) => {
            if (clubs[player.club]) {
                clubs[player.club] += 1;
            } else {
                clubs[player.club] = 1;
            }
        });
        return clubs;
    };

    let barChartData = countPlayersByClub(players);
    barChartData = Object.keys(barChartData).map((club) => {
        return {
            club: club,
            count: barChartData[club],
        };
    });

    const customTickFormatter = (value) => {
        // Maximum length for the club name before truncation
        const maxLength = 10; // Adjust as needed

        // Check if the club name exceeds the maximum length
        if (value.length > maxLength) {
            // Truncate the club name and append ellipsis
            return value.substring(0, maxLength - 3) + '...';
        }
        return value;
    };

    const yTickFormatter = (value) => {
        return Math.round(value); // Round to the nearest integer
    };

    if (loading) {
        return <div>Loading...</div>;
    }

    return (
        <div>
            <h2>Bar Chart</h2>
            <BarChart 
                dataset={barChartData}
                xAxis={[{ scaleType: 'band', dataKey: 'club', tickFormater: customTickFormatter, tick: {style: {whiteSpace: 'nowrap', textOverflow: 'ellipsis', overflow: 'hidden', maxWidth: 100}}}]}
                series={[{ scaleType: 'band', dataKey: 'count'}]}
                width={1000}
                height={400}
            />
        </div>
    );
}
