import { DataGrid } from '@mui/x-data-grid';
import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useCombinedContext } from './context';

export function Team() {
    const [content, setContent] = useState(
        <TeamsList displayForm={displayForm} />
    );

    function displayList() {
        setContent(<TeamsList displayForm={displayForm} />);
    }

    function displayForm(team) {
        setContent(<TeamsForm team={team} displayList={displayList} />);
    }

    return (
        <div className="container">
            {content}
        </div>
    );
}

export function TeamsList(props) {
    const { teamsList, setTeamsList } = useCombinedContext();
    const navigate = useNavigate();

    function fetchTeams() {
        fetch('http://127.0.0.1:8000/teams/', {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': 'Bearer ' + localStorage.getItem('token'),
            }
        })
            .then((response) => {
                if (!response.ok) {
                    return response.json().then((error) => {
                        throw new Error(error.detail || 'Failed to fetch teams');
                    });
                }
                return response.json();
            })
            .then((data) => {
                setTeamsList(data);
            })
            .catch((error) => {
                console.error('Error fetching teams:', error);
            });
    }

    useEffect(() => {
        fetchTeams();
    }, []);
    
    function deleteTeam(id) {
        fetch(`http://127.0.0.1:8000/teams/${id}`, {
            method: 'DELETE',
        })
            .then((response) => {
                if (!response.ok) {
                    return response.json().then((data) => {
                        throw new Error('Failed to delete team');
                    });
                }
                fetchTeams();
                return response.json();
            })
            .catch((error) => {
                console.error('Error deleting team:', error);
            });
    }

    const columns = [
        { field: 'name', headerName: 'Name', width: 150 },
        { field: 'country', headerName: 'Country', width: 150 },
        { field: 'number_of_trophies', headerName: 'Trophies', width: 150 },
        { field: 'edit', headerName: '', width: 70,
            renderCell: (params) => {
                return <button onClick={() => props.displayForm ( params.row )} type= "button" className="btn btn-primary">Edit</button>
            },
        },
        { field: 'delete', headerName: '', width: 70,
            renderCell: (params) => {
                return <button onClick={() => deleteTeam ( params.row.id )} type= "button" className="btn btn-danger btn-sm">Delete</button>
            },
        },
    ];

    function handleDoubleClick(row) {
        navigate(`/team/${row.id}`);
    }

    return (
        <>
            <h2 className= "text-center mb-3"> List of Players </h2>
            <button onClick={() => props.displayForm({}) } type="btn btn-primary me-2">Add Team</button>
            <button onClick={() => fetchTeams() } type="btn btn-outline-primary me-2">Refresh</button>
            <div style={{ height: 400, width: '70%' }}>
                <DataGrid
                    rows={teamsList}
                    columns={columns}
                    // pageSize={5}
                    initialState={{ 
                        pagination: { paginationModel: { pageSize: 5 } },
                    }}
                    pageSizeOptions={[5, 10, 20]}
                    rowKey = { (row) => row.id}
                    onRowDoubleClick={handleDoubleClick}
                />
            </div>
        </>
    )
}

function TeamsForm(props) {
    function handleSubmit(event) {
        event.preventDefault();
        const formData = new FormData(event.target);
        const data = Object.fromEntries(formData.entries());
        if (!data.name || !data.country || !data.number_of_trophies) {
            alert('All fields are required');
            console.log(data.name);
            return;
        }

        if (data.id) {
            fetch(`http://127.0.0.1:8000/teams/${data.id}`, {
                method: 'PUT',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(data),
            })
                .then((response) => {
                    if (!response.ok) {
                        throw new Error('Failed to update team');
                    }
                    props.displayList();
                })
                .catch((error) => {
                    console.error('Error updating team:', error);
                });
        } else {
            fetch('http://127.0.0.1:8000/teams/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    "Authorization": "Bearer " + localStorage.getItem("token"),
                },
                body: JSON.stringify(data),
            })
                .then((response) => {
                    if (!response.ok) {
                        throw new Error('Failed to create team');
                    }
                    props.displayList();
                })
                .catch((error) => {
                    console.error('Error creating team:', error);
                });
        }
    }

    return (
        <>
            <h2 className='mt-3'> {props.team.id ? 'Edit' : 'Add'} Team </h2>
            <div className="row">
                <div className="col-md-6">
                <form onSubmit={(event) => handleSubmit(event)}>
                    {props.team.id && <input type="hidden" name="id" value={props.team.id} />}

                    <div className="mb-3">
                        <label htmlFor="name" className="form-label">Name</label>
                        <input type="text" name="name" className="form-control" defaultValue={props.team.name} />
                    </div>

                    <div className="mb-3">
                        <label htmlFor="country" className="form-label">Country</label>
                        <input type="text" name="country" className="form-control" defaultValue={props.team.country} />
                    </div>

                    <div className="mb-3">
                        <label htmlFor="number_of_trophies" className="form-label">Trophies</label>
                        <input type="number" name="number_of_trophies" className="form-control" defaultValue={props.team.number_of_trophies} />
                    </div>

                    <button type="submit" className="btn btn-primary">Save</button>
                    <button type="button" onClick={props.displayList} className="btn btn-secondary">Cancel</button>

                </form>
                </div>
            </div>
            
        </>
    )
}