import React, { useState } from 'react';

 const SubmitListingForm =()=> {
    const [formData, setFormData] = useState({
        name: '',
        description: '',
        startPrice: '',
        quantity: '',
        shippingCosts: '',
        expiration: '',
        photo: null
    });

    const handleChange = (e) => {
        const { name, value, type, files } = e.target;
        setFormData(prevFormData => ({
            ...prevFormData,
            [name]: type === 'file' ? files[0] : value
        }));
    };

    const handleSubmit = (e) => {
        e.preventDefault();
        // 在这里处理表单数据提交的逻辑
        console.log(formData);
    };

    return (
        <div className="container pt-5">
            <div className="row mt-2">
                <div className="col">
                    <h1>Submit a Listing</h1>
                </div>
            </div>
            <div className="row mt-2">
                <h4>Fields marked with a red asterisk (<span style={{ color: 'red' }}>*</span>) are required.</h4>
            </div>
            <form onSubmit={handleSubmit} encType="multipart/form-data">
                <div className="row mt-2">
                    <div className="col-4">
                        <label htmlFor="name" className="form-label">Enter your item's name:<strong style={{ color: 'red' }}>*</strong></label>
                        <input type="text" className="form-control" id="name" name="name" value={formData.name} onChange={handleChange} />
                    </div>
                </div>
                <div className="row mt-2">
                    <div className="col-4">
                        <label htmlFor="description" className="form-label">Enter your item's description:<strong style={{ color: 'red' }}>*</strong></label>
                        <input type="text" className="form-control" id="description" name="description" value={formData.description} onChange={handleChange} />
                    </div>
                </div>
                <div className="row mt-2">
                    <div className="col-4">
                        <label htmlFor="startPrice" className="form-label">Enter a start price amount:<strong style={{ color: 'red' }}>*</strong></label>
                        <input type="number" className="form-control" id="startPrice" name="startPrice" value={formData.startPrice} onChange={handleChange} />
                    </div>
                </div>
                <div className="row mt-2">
                    <div className="col-4">
                        <label htmlFor="quantity" className="form-label">Enter the quantity:<strong style={{ color: 'red' }}>*</strong></label>
                        <input type="number" className="form-control" id="quantity" name="quantity" value={formData.quantity} onChange={handleChange} />
                    </div>
                </div>
                <div className="row mt-2">
                    <div className="col-4">
                        <label htmlFor="shippingCosts" className="form-label">Enter the shipping costs:<strong style={{ color: 'red' }}>*</strong></label>
                        <input type="number" className="form-control" id="shippingCosts" name="shippingCosts" value={formData.shippingCosts} onChange={handleChange} />
                    </div>
                </div>
                <div className="row mt-2">
                    <div className="col-4">
                        <label htmlFor="expiration" className="form-label">Set an expiration date for your auction:<strong style={{ color: 'red' }}>*</strong></label>
                        <input type="date" className="form-control" id="expiration" name="expiration" value={formData.expiration} onChange={handleChange} />
                    </div>
                </div>
                <div className="row mt-2">
                    <div className="col-4">
                        <label htmlFor="photo" className="form-label">Include a photo of your item:</label>
                        <input className="form-control" type="file" id="photo" name="photo" accept="image/*" onChange={handleChange} />
                    </div>
                </div>
                <div className="row my-5">
                    <div className="col-4">
                        <button className="btn main-button" type="submit">Submit Listing</button>
                    </div>
                </div>
            </form>
        </div>
    );
}

export default SubmitListingForm;
