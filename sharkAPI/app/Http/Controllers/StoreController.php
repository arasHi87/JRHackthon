<?php

namespace App\Http\Controllers;

use App\Models\Store;
use App\Models\Feedback;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\Validator;

class StoreController extends Controller
{
    public function list()
    {
        return response()->json(Store::get([
            'id', 'name', 'address', 'rating', 'image', 'longitude', 'latitude'
        ]));
    }

    public function index(Request $request)
    {
        $store_id = $request->id;
        $feedbacks = Feedback::where('store_id', $store_id)->get(['username', 'rating', 'comment']);
        $stores = Store::find($request->id);
        $stores->feedback = $feedbacks;

        return response()->json($stores, 200);
    }

    public function sort(Request $request)
    {
        $data = $request->all();
        $latitude = $data['latitude'];
        $longitude = $data['longitude'];
        $stores = Store::get(['id', 'name', 'address', 'rating', 'image', 'longitude', 'latitude']);

        foreach ($stores as &$store) {
            $store->distance = pow($store->longitude - $longitude, 2)
                             + pow($store->latitude - $latitude, 2);
        }

        $stores = $stores->toArray();

        usort($stores, function ($x, $y) {
            return $x['distance'] > $y['distance'];
        });

        return response()->json(array_slice($stores, 0, 100), 200);
    }

    public function add(Request $request)
    {
        $data = $request->all();

        if (Store::where(['address', $data['address']])->first()) {
            return response()->json([], 200);
        }

        Store::create([
            'name' => $data['name'],
            'address' => $data['address'],
            'rating' => $data['rating'],
            'latitude' => $data['latitude'],
            'longitude' => $data['longitude'],
            'image' => $data['image']
        ]);

        return response()->json([], 200);
    }

    public function search(Request $request)
    {
        $data = $request->all();
        $stores = Store::where('name', 'like', '%' . $data['keywords'][0] . '%');

        foreach ($data['keywords'] as $keyword) {
            $stores->orWhere('name', 'like', '%' . $keyword . '%')
                   ->orWhere('address', 'like', '%' . $keyword . '%');
        }

        return response()->json($stores->get(['id', 'name', 'address']));
    }
}
