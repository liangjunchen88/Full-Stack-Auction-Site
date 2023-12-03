import React, { useState, useEffect } from "react";
import axios from "axios";
import config from "../config";

// StarRating component showing the rating for the user
function StarRating({ rating }) {
  const stars = [];
  for (let i = 1; i <= rating; i++) {
    stars.push(
      <span key={i} className={i <= rating ? "text-warning" : "text-muted"}>
        &#9733; {/* Star character */}
      </span>
    );
  }
  return <div>{stars}</div>;
}

function Profile({ user }) {
  const [activeListings, setActiveListings] = useState([]);
  const [shoppingCart, setShoppingCart] = useState([]);
  const [bidHistory, setBidHistory] = useState([]);
  const [userInfo, setUserInfo] = useState([]);
  const [activeUsers, setActiveUsers] = useState([]);

  useEffect(() => {
    if (!user || !user.id) return;
    axios
      .get(`${config.userServiceUrl}/user/${user.id}/profile`)
      .then((response) => {
        if (response.data.success) {
          setUserInfo(response.data.data);
        }
      })
      .catch((error) => console.log(error));

    axios
      .get(`${config.userServiceUrl}/user/${user.id}/active-listings`)
      .then((response) => {
        setActiveListings(response.data.data);
      })
      .catch((error) => console.log(error));

    axios
      .get(`${config.userServiceUrl}/user/${user.id}/bid-history`)
      .then((response) => {
        setBidHistory(response.data.data);
      })
      .catch((error) => console.log(error));

    axios
      .get(`${config.userServiceUrl}/user/${user.id}/active-users`)
      .then((response) => {
        if (response.data.success) {
          setActiveUsers(response.data.data);
        }
      })
      .catch((error) => console.log(error));

    axios
      .get(`${config.userServiceUrl}/user/${user.id}/shopping-cart`)
      .then((response) => {
        setShoppingCart(response.data.data);
      })
      .catch((error) => console.log(error));
  }, [user, user.id]);

  if (!userInfo) {
    return <div>Loading...</div>;
  } else {
    console.log(userInfo);
  }

  return (
    <div className="container pt-5">
      <h1>{userInfo.firstName}'s Profile</h1>

      {/* Basic info of the user */}
      <div className="mt-4">
        <h4 style={{ color: "maroon" }}>Profile Details</h4>
        <div className="row">
          <div className="col-4">
            <label>First Name</label>
            <input
              type="text"
              className="form-control"
              value={userInfo.firstName}
              disabled
            />
          </div>
          <div className="col-4">
            <label>Last Name</label>
            <input
              type="text"
              className="form-control"
              value={userInfo.lastName}
              disabled
            />
          </div>
        </div>
        <div className="row mt-2">
          <div className="col-4">
            <label>Email</label>
            <input
              type="email"
              className="form-control"
              value={userInfo.email}
              disabled
            />
          </div>
        </div>
        <div className="row mt-2">
          <div className="col-4">
            <label>Username</label>
            <input
              type="text"
              className="form-control"
              value={userInfo.userName}
              disabled
            />
          </div>
        </div>
        <div className="row mt-2">
          <div className="col-4">
            <label>Date Joined</label>
            <input
              type="text"
              className="form-control"
              value={new Date(userInfo.dateJoined).toLocaleDateString()}
              disabled
            />
          </div>
        </div>
        <div className="row mt-2">
          <div className="col-4">
            <label>User Rating</label>
            <div className="form-control" style={{ padding: "7px" }}>
              <StarRating rating={parseFloat(userInfo.rating)} />
              <small>{userInfo.rating}/5.0</small>
            </div>
          </div>
        </div>
        <div className="row mt-2">
          <div className="col-4">
            <label>Account Status</label>
            <input
              type="text"
              className="form-control"
              value={userInfo.isActive ? "Active" : "Inactive"}
              disabled
            />
          </div>
        </div>
        <div className="row mt-2">
          <div className="col-4">
            <label>Admin Status</label>
            <input
              type="text"
              className="form-control"
              value={userInfo.isAdmin ? "Admin" : "User"}
              disabled
            />
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
                  {/* opration button */}
                  <button className="btn btn-danger">Cancel</button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      {/* Bid history Table - Only render for normal users */}
      {!user.isAdmin && (
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
              {bidHistory.map((bid) => (
                <tr key={bid.bidID}>
                  <td>{new Date(bid.bidDate).toLocaleDateString()}</td>
                  <td>{bid.name}</td>
                  <td>{bid.bidAmt}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}

      {/* User Management Table - for all users */}
      <div className="mt-5">
        <h4 style={{ color: "maroon" }}>User Management</h4>
        <table className="table table-striped table-hover">
          <thead>
            <tr>
              <th>#</th>
              <th>User</th>
              <th>First Name</th>
              <th>Last Name</th>
              <th>Date Joined</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            {activeUsers.map((user, index) => (
              <tr key={user.userID}>
                <th scope="row">{index + 1}</th>
                <td>{user.userName}</td>
                <td>{user.firstName}</td>
                <td>{user.lastName}</td>
                <td>{new Date(user.dateJoined).toLocaleDateString()}</td>
                <td>
                  {/* operation button */}
                  <button className="btn btn-danger">Delete</button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      {/* Shopping Cart Table - Only render for normal users */}
      {!user.isAdmin && (
        <div className="mt-5">
          <h4 style={{ color: "maroon" }}>Shopping Cart</h4>
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
              {shoppingCart.map((listing, index) => (
                <tr key={listing.listingID}>
                  <th>{index + 1}</th>
                  <td>{listing.name}</td>
                  <td>{listing.bidAmt}</td>
                  <td>{listing.startPrice}</td>
                  <td>{new Date(listing.endDate).toLocaleDateString()}</td>
                  <td>
                    {/* opration button */}
                    <button className="btn btn-danger">Cancel</button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
}

export default Profile;
