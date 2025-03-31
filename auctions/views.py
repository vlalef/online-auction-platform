from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.contrib import messages
from decimal import Decimal, InvalidOperation
from .models import User, Listing, Category, Bid, Comment
from .forms import ListingForm, BidForm, CommentForm


def index(request):
    return render(request, "auctions/index.html", {
        "listings": Listing.objects.filter(is_active=True)
    })


def login_view(request):
    if request.method == "POST":

        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")


@login_required
def create_listing(request):
    if request.method == "POST":
        title = request.POST["title"]
        description = request.POST["description"]
        starting_bid = float(request.POST["starting_bid"])
        image_url = request.POST.get("image_url", "")
        category_id = request.POST.get("category")

        listing = Listing(
            title=title,
            description=description,
            starting_bid=starting_bid,
            current_price=starting_bid,
            image_url=image_url,
            creator=request.user,
            is_active=True
        )

        if category_id:
            listing.category = Category.objects.get(pk=category_id)

        listing.save()
        return redirect("index")

    return render(request, "auctions/create.html", {
        "categories": Category.objects.all()
    })


@login_required
def listing(request, listing_id):
    listing = get_object_or_404(Listing, pk=listing_id)
    bid_form = BidForm()
    comment_form = CommentForm()
    comments = Comment.objects.filter(listing=listing)
    is_watched = request.user.is_authenticated and listing in request.user.watchlist.all()

    if request.method == "POST" and request.user.is_authenticated:
        if "bid" in request.POST:
            bid_amount = request.POST.get('bid_amount')
            try:
                bid_amount = Decimal(bid_amount)
                if not listing.is_active:
                    messages.error(request, "This auction is closed!")
                elif bid_amount > listing.current_price:
                    bid = Bid(user=request.user, listing=listing, amount=bid_amount)
                    bid.save()
                    listing.current_price = bid_amount
                    listing.highest_bid = bid_amount
                    listing.highest_bidder = request.user
                    listing.save()
                    messages.success(request, "Bid placed successfully!")
                else:
                    messages.error(request, "Bid must be higher than current price!")
            except (InvalidOperation, TypeError, ValueError):
                messages.error(request, "Invalid bid amount!")

        elif "comment" in request.POST:
            comment_form = CommentForm(request.POST)
            if comment_form.is_valid():
                comment = comment_form.save(commit=False)
                comment.user = request.user
                comment.listing = listing
                comment.save()
                messages.success(request, "Comment added successfully!")

    return render(request, "auctions/listing.html", {
        "listing": listing,
        "bid_form": bid_form,
        "comment_form": comment_form,
        "comments": comments,
        "is_watched": is_watched
    })


@login_required
def place_bid(request, listing_id):
    listing = get_object_or_404(Listing, pk=listing_id)
    if request.method == "POST":
        bid_amount = request.POST.get('bid_amount')
        if bid_amount:
            bid_amount = float(bid_amount)
            if bid_amount > listing.current_price:
                listing.current_price = bid_amount
                listing.highest_bid = bid_amount
                listing.highest_bidder = request.user
                listing.save()
                messages.success(request, "Bid placed successfully!")
            else:
                messages.success(request, "Bid must be higher than the current price.")
        else:
            messages.error(request, "Invalid bid amount.")
    return redirect('listing', listing_id=listing_id)


@login_required
def place_bid_index(request, listing_id):
    listing = get_object_or_404(Listing, pk=listing_id)
    if request.method == "POST":
        bid_amount = request.POST.get('bid_amount')
        if bid_amount:
            try:
                bid_amount = float(bid_amount)
                if bid_amount > listing.current_price:
                    listing.current_price = bid_amount
                    listing.highest_bid = bid_amount
                    listing.highest_bidder = request.user
                    listing.save()
                    messages.success(request, "Bid placed successfully!")
                else:
                    messages.warning(request, "Bid must be higher than the current price.")
            except ValueError:
                messages.error(request, "Invalid bid amount.")
        else:
            messages.error(request, "Invalid bid amount.")
    return redirect('index')


@login_required
def watchlist(request):
    listings = request.user.watchlist.all()
    return render(request, "auctions/watchlist.html", {
        "listings": listings
    })


def add_to_watchlist_index(request, listing_id):
    if request.method == "POST":
        listing = get_object_or_404(Listing, pk=listing_id)
        request.user.watchlist.add(listing)
        messages.success(request, "Added to watchlist successfully!")
        return redirect('index')
    return redirect('index')


@login_required
def add_to_watchlist_detail(request, listing_id):
    if request.method == "POST":
        listing = get_object_or_404(Listing, pk=listing_id)
        request.user.watchlist.add(listing)
        messages.success(request, "Added to watchlist successfully!")
        return redirect('listing', listing_id=listing_id)
    return redirect('listing', listing_id=listing_id)


@login_required
def toggle_watchlist(request, listing_id):
    listing = get_object_or_404(Listing, pk=listing_id)
    if listing in request.user.watchlist.all():
        request.user.watchlist.remove(listing)
        messages.success(request, "Removed from watchlist!")
    else:
        request.user.watchlist.add(listing)
        messages.success(request, "Added to watchlist!")
    return redirect('listing', listing_id=listing_id)

@login_required
def remove_from_watchlist(request, listing_id):
    listing = get_object_or_404(Listing, pk=listing_id)
    request.user.watchlist.remove(listing)
    messages.success(request, "Removed from watchlist!")
    return redirect('watchlist')


@login_required
def categories_view(request):
    categories = Category.objects.all()
    return render(request, "auctions/categories.html", {
        "categories": categories
    })


@login_required
def category_view(request, category_id):
    category = get_object_or_404(Category, pk=category_id)
    listings = Listing.objects.filter(category=category, is_active=True)
    return render(request, "auctions/category.html", {
        "category": category,
        "listings": listings
    })


@login_required
def open_auction(request, listing_id):
    listing = get_object_or_404(Listing, pk=listing_id)
    if request.user == listing.creator and not listing.is_active:
        listing.is_active = True
        listing.save()
        messages.success(request, "Auction reopened successfully!")
    return redirect('listing', listing_id=listing_id)


@login_required
def close_auction(request, listing_id):
    listing = get_object_or_404(Listing, pk=listing_id)
    if request.user == listing.creator:
        highest_bid = Bid.objects.filter(listing=listing).first()
        if highest_bid:
            listing.winner = highest_bid.user
        listing.is_active = False
        listing.save()
        messages.success(request, "Auction closed successfully!")
    return redirect('listing', listing_id=listing_id)


@login_required
def create_category(request):
    if request.method == "POST":
        name = request.POST.get("name")
        if name:
            Category.objects.create(name=name)
            messages.success(request, "Category created successfully!")
        else:
            messages.error(request, "Category name is required!")
    return redirect('categories')


@login_required
def delete_category(request, category_id):
    if request.method == "POST":
        category = get_object_or_404(Category, pk=category_id)
        if Listing.objects.filter(category=category).exists():
            messages.error(request, "Cannot delete category that has listings!")
        else:
            category.delete()
            messages.success(request, "Category deleted successfully!")
    return redirect('categories')
