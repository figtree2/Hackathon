const mongoose = require('mongoose')

const schema = new mongoose.Schema({
    _id: {
        type: String,
        required: false
    },

    title:{
        type: String,
        require: false
    },
    content:{
        type: String,
        require: false
    },
    address:{
        type: String,
        require: false
    },
    latitude:{
        type: String,
        require: false
    },
    longitude:{
        type: String,
        require: false
    }
})

module.exports = mongoose.model('form', schema, 'form')