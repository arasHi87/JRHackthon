<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;

class Store extends Model
{
    /**
     * The attributes that are mass assignable.
     *
     * @var array
     */
    protected $fillable = [
        'name', 'address', 'rating', 'latitude', 'longitude', 'image'
    ];

    protected $hidden = ["created_at", "updated_at"];
}
