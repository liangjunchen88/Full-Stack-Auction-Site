import React, { useState, useEffect } from 'react';
import axios from 'axios';
import config from "../config";

function Profile({ user }) {
    const [activeListings, setActiveListings] = useState([]);
    const [bidHistory, setBidHistory] = useState([]);
    const [userInfo, setUserInfo] = useState([]);

    useEffect(() => {
        if (!user || !user.id) return;
        axios.get(`${config.userServiceUrl}/user/${user.id}/profile`)
            .then(response => {
                if (response.data.success) {
                    setUserInfo(response.data.data);
                }
            })
            .catch(error => console.log(error));

        axios.get(`${config.userServiceUrl}/user/${user.id}/active-listings`)
            .then(response => {
                setActiveListings(response.data.data);
            })
            .catch(error => console.log(error));

        axios.get(`${config.userServiceUrl}/user/${user.id}/bid-history`)
            .then(response => {
                setBidHistory(response.data.data);
            })
            .catch(error => console.log(error));
    }, [user, user.id]);

    if (!userInfo) {
        return <div>Loading...</div>;
    } else {
        console.log(userInfo)
    }

    return (
        <div className="container pt-5">
            <h1>{userInfo.firstName}'s Profile</h1>

            {/* 用户基本信息 */}
            <div className="mt-4">
                <h4 style={{ color: "maroon" }}>Profile Details</h4>
                <div className="row">
                    <div className="col-4">
                        <label>First Name</label>
                        <input type="text" className="form-control" value={userInfo.firstName} disabled />
                    </div>
                    <div className="col-4">
                        <label>Last Name</label>
                        <input type="text" className="form-control" value={userInfo.lastName} disabled />
                    </div>
                </div>
                <div className="row mt-2">
                    <div className="col-4">
                        <label>Email</label>
                        <input type="email" className="form-control" value={userInfo.email} disabled />
                    </div>
                </div>
                <div className="row mt-2">
                    <div className="col-4">
                        <label>Username</label>
                        <input type="text" className="form-control" value={userInfo.userName} disabled />
                    </div>
                </div>
                <div className="row mt-2">
                    <div className="col-4">
                        <label>Date Joined</label>
                        <input type="text" className="form-control" value={new Date(userInfo.dateJoined).toLocaleDateString()} disabled />
                    </div>
                </div>
                <div className="row mt-2">
                    <div className="col-4">
                        <label>User Rating</label>
                        <input type="text" className="form-control" value={userInfo.rating} disabled />
                    </div>
                </div>
                <div className="row mt-2">
                    <div className="col-4">
                        <label>Account Status</label>
                        <input type="text" className="form-control" value={userInfo.isActive ? 'Active' : 'Inactive'} disabled />
                    </div>
                </div>
                <div className="row mt-2">
                    <div className="col-4">
                        <label>Admin Status</label>
                        <input type="text" className="form-control" value={userInfo.isAdmin ? 'Admin' : 'User'} disabled />
                    </div>
                </div>
            </div>

            <div className="mt-5">
                <h4 style={{ color: "maroon" }}>Active Listings</h4>
                <table className="table table-striped table-hover">
                    <thead>
                        <tr>
                            <th>#</th>
                            <th>Item</th>
                            <th>Current Bid</th>
                            <th>Start Price</th>
                            <th>Expires</th>
                            <th>Actions</th>
                        </tr>
                    </thead>
                    <tbody>
                        {activeListings.map((listing, index) => (
                            <tr key={listing.listingID}>
                                <th>{index + 1}</th>
                                <td>{listing.name}</td>
                                <td>{listing.bidAmt}</td>
                                <td>{listing.startPrice}</td>
                                <td>{new Date(listing.endDate).toLocaleDateString()}</td>
                                <td>
                                    {/* 操作按钮 */}
                                    <button className="btn btn-danger">Cancel</button>
                                </td>
                            </tr>
                        ))}
                    </tbody>
                </table>
            </div>

            <div className="mt-5">
                <h4 style={{ color: "maroon" }}>Bid History</h4>
                <table className="table table-striped table-hover">
                    <thead>
                        <tr>
                            <th>Date Placed</th>
                            <th>Item</th>
                            <th>Bid Amount</th>
                        </tr>
                    </thead>
                    <tbody>
                        {bidHistory.map(bid => (
                            <tr key={bid.bidID}>
                                <td>{new Date(bid.bidDate).toLocaleDateString()}</td>
                                <td>{bid.name}</td>
                                <td>{bid.bidAmt}</td>
                            </tr>
                        ))}
                    </tbody>
                </table>
            </div>
        </div>
    );
}

export default Profile;
