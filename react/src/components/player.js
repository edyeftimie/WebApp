import React, { useEffect, useState } from "react";
import { DataGrid } from "@mui/x-data-grid";
import { useNavigate } from "react-router-dom";
import { useCombinedContext } from "./context";

export function Player() {
    const [content, setContent] = useState(
        <PlayersList displayForm={displayForm}/>
    );

    function displayList() {
        setContent(<PlayersList displayForm={displayForm}/>);
    }

    function displayForm(player) {
        setContent(<PlayersForm player={player} displayList={displayList}/>);
    }

    return (
        <div className="container my-5">
            { content }
        </div>
    );
}

export function PlayersList(props) {
    const { playersList, setPlayersList } = useCombinedContext();
    const navigate = useNavigate();
    const [ws, setWs] = useState(null);

    useEffect(() => {
        const socket = new WebSocket('ws://localhost:8000/ws');

        socket.onopen = () => {
            console.log('WebSocket Client Connected');
            setWs(socket);
        };

        socket.onmessage = (message) => {
            console.log(message);
            // console.log('WebSocket Client Received Message:', message.data);
            fetchPlayers();
        };

        socket.onclose = () => {
            console.log('WebSocket Client Disconnected');
        };

        return () => {
            if (ws) {
                ws.close();
                setWs(null);
            }
            // socket.close();
        };
    }, []);

    // function fetchInitialData() {
    //     Promise.all([fetchPlayers(), fetchTeams()])
    //         .then (([players, teams]) => {
    //             setPlayersList(players);
    //             setTeamsList(teams);
    //         })
    //         .catch((error) => {
    //             console.error('Error fetching initial data:', error);
    //         });
    // }

    const fetchPlayersRef = React.useRef(fetchPlayers);

    useEffect(() => {
        fetchPlayersRef.current = fetchPlayers;
    });

    function fetchPlayers() {
        fetch('http://127.0.0.1:8000/players/')
            .then(response => {
                if (!response.ok) {
                    return response.json().then((error) => {
                        throw new Error(error.detail);
                    });
                    // throw new Error('Network response was not ok');
                }
                return response.json();
            })
            .then(data => {
                setPlayersList(data);
            })
            .catch(error => (
                console.error('There has been a problem with your fetch operation:', error))
                );
    }

    useEffect (() => {
        fetchPlayers();
    }, []);

    function deletePlayer(id) {
        fetch('http://127.0.0.1:8000/players/' + id, {
            method: 'DELETE',
        })
            .then(response => {
                if (!response.ok) {
                    return response.json().then((error) => {
                        throw new Error(error.detail);
                    }); 
                }
                return response.json();
            })
            .then(data => {
                fetchPlayers();
            })
            .catch(error => (
                window.alert(error.message),
                console.error('There has been a problem with your fetch operation:', error))
            );
    }

    const columns = [
        { field: 'name', headerName: 'Name', width: 150, sortable: true, filterable: true, editable: false },
        { field: 'age', headerName: 'Age', width: 150, sortable: true, filterable: true, editable: false },
        { field: 'team_id', headerName: 'Team_Id', width: 150, sortable: true, filterable: true, editable: false },
        // { field: 'createdAt', headerName: 'Created At', width: 150, sortable: true, filterable: false, editable: false},
        { field: 'edit', headerName: '', width: 70, sortable: false, filterable: false,
            renderCell: (params) => {
                return <button onClick={() => props.displayForm( params.row)} type="button" className="btn btn-primary btn-sm me-2" >Edit</button>
            }, 
        },
        { field: 'delete', headerName: '', width: 70, sortable: false, filterable: false,
            renderCell: (params) => {
                return <button onClick={() => deletePlayer(params.row.id)} type="button" className="btn btn-danger btn-sm" >Delete</button>
            }, 
        },
        //{ field: 'createdAt', headerName: 'Created At', width: 150, sortable: true, filterable: false, editable: false},
        // { field: 'details', headerName: '', width: 70, sortable: false, filterable: false,
        //     renderCell: (params) => {
        //         return <button onClick={() => navigate(`/player/${params.row.id}`, { state: { player: params.row } })} type="button" className="btn btn-info btn-sm" >Details</button>
        //     }, 
        // },
    ];

    function handleDoubleClick(params) {
        navigate(`/player/${params.row.id}`, { state: { player: params.row } });
    };

    function handleChartClick(params) {
        if (playersList.length === 0) {
            alert('No players to display');
            return;
        }
        navigate(`/chart`, { state: {listOf: playersList} });
    }
    const [youngest, setYoungest] = useState(null);

    function youngestPlayer(params) {
        if (playersList.length === 0) {
            alert('No players to display');
            return;
        }
        let young = null
        let listOf = playersList;
        listOf.map ((player) => {
            if (young == null || player.age < young.age) {
                young = player;
            }
        });
        setYoungest(young);
    }

    const { teamsList } = useCombinedContext();

    return (
        <>
            <h2 className= "text-center mb-3"> List of Players </h2>
            <button onClick={() => props.displayForm({}) } type="btn btn-primary me-2">Add Player</button>
            <button onClick={() => fetchPlayers() } type="btn btn-outline-primary me-2">Refresh</button>
            <button onClick={() => handleChartClick()} type="btn btn-outline-primary me-2">Show Chart</button>
            {/* <button onClick={() => youngestPlayer() } type="btn btn-outline-primary me-2">Show youngest player</button> */}
            <div>
                {youngest && (<div>
                    <h3>Youngest player</h3>
                    <p>Name: {youngest.name}</p>
                </div>)}
            </div>
            <DataGrid
                rows = {playersList.map((playerr) => {
                    return {
                        id: playerr.id,
                        name: playerr.name,
                        age: playerr.age,
                        // team_id: playerr.team_id,
                        team_id: teamsList.find((team) => team.id === playerr.team_id)?.name || 'Unknown',
                        createdAt: playerr.createdAt,
                    };
                })}
                columns={columns}
                style={{height: 400, width: '70%'}}
                initialState={{ 
                    pagination: { paginationModel: { pageSize: 5 } },
                }}
                pageSizeOptions={[5, 10, 20]}
                rowKey={(row) => row.id}
                onCellDoubleClick={handleDoubleClick}
            />
        </>
    );
}

function PlayersForm(props) {
    function handleSubmit(event) {
        // prevent default form submission
        event.preventDefault();
        // read form data
        const formData = new FormData(event.target);
        // convert form data to object
        const data = Object.fromEntries(formData.entries());
        // validate data
        if (!data.name || !data.age || !data.team_id) {
        // if (!data.name || !data.age) {
            alert('Please enter all fields');
            return;
        }

        if (props.player.id) {
            //update player
            // console.log("update player");
            fetch('http://127.0.0.1:8000/players/' + props.player.id , {
                method: 'PUT',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(data),
            })
                .then ((response) => {
                    console.log(data);
                    if (!response.ok) {
                        return response.json().then((error) => {
                            throw new Error(error.detail);
                        });
                        // throw new Error('Network response was not ok');
                    }
                    return response.json();
                })
                .then((data) => {
                    // console.log(data);
                    props.displayList();
                })
                .catch((error) => (
                    window.alert(error.message),
                    console.error('There has been a problem with your fetch operation:', error)))
                    ;
        } else {
            //create new player
            // console.log("create new player");
            // data.createdAt = new Date().toISOString().slice(0, 10);
            // fetch ('http://localhost:8000/players/?team_id=' + data.team_id, {
            fetch ('http://localhost:8000/players/' + data.team_id, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(data),
            })
                .then ((response) => {
                    // console.log(data);
                    if (!response.ok) {
                        return response.json().then((error) => {
                            throw new Error(error.detail);
                        });
                    }
                    return response.json();
                })
                .then((data) => {
                    // console.log(data);
                    props.displayList();
                })
                .catch((error) => (
                    window.alert(error.message),
                    //i want to catch the the http exception and display the details of the error
                    console.error('There has been a problem with your fetch operation:', error))
                    );
        }
    }

    return (
        <>
            <h2 className = "text-center mb-3">{props.player.id ? "Edit player": "Add new player" }</h2>
            {/* <button onClick={() => props.displayList()} type = "btn btn-secondary me-2"> Cancel</button> */}

            <div className="row">
                <div className="col-lg-6 mx-auto">
                <form onSubmit={(event) => handleSubmit(event)}>
                    {props.player.id && <div className="row mb-3">
                        <label className="col-sm-4 col-form-label">ID</label>
                        <div className="col-sm-8">
                            <input readOnly className="form-control-plaintext"
                                name = "id"
                                defaultValue={props.player.id} />
                        </div>
                    </div>}

                    <div className="row mb-3">
                        <label className="col-sm-4 col-form-label">Name</label>
                        <div className="col-sm-8">
                            <input className="form-control"
                                name = "name"
                                defaultValue={props.player.name} />
                        </div>
                    </div>
                    <div className="row mb-3">
                        <label className="col-sm-4 col-form-label">Age</label>
                        <div className="col-sm-8">
                            <input className="form-control"
                                name = "age"
                                defaultValue={props.player.age} />
                        </div>
                    </div>
                    {props.player.id ? (
                        <div className="row mb-3">
                            <label className="col-sm-4 col-form-label">Team</label>
                            <div className="col-sm-8">
                                <input readOnly className="form-control"
                                    name = "team_id"
                                    defaultValue={props.player.team_id} />
                            </div>
                        </div>
                        ) : (
                        <div className="row mb-3">
                            <label className="col-sm-4 col-form-label">Team</label>
                            <div className="col-sm-8">
                                <input className="form-control"
                                    name = "team_id"
                                    defaultValue={props.player.team_id} />
                            </div>
                        </div>
                        )
                    }
                    <div className="row">
                        <div className="offset-sm-4 col-sm-4 d-grid">
                            <button type="submit" className="btn btn-primary btn-sm me-3">Save</button>
                        </div>
                        <div className="col-sm-4 d-grid">
                            <button onClick={() => props.displayList()} type="button" className="btn btn-secondary btn-sm">Cancel</button>
                        </div>
                    </div>
                </form>
                </div>
            </div>
        </>
    )
}