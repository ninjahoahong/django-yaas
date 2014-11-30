from decimal import Decimal, InvalidOperation

__author__ = 'Duong Duc Anh'

from datetime import datetime
from django.contrib import auth
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core import serializers
from django.core.urlresolvers import reverse
from django.db.models.sql.aggregates import Max
from django.http import HttpResponseRedirect, HttpResponse, Http404, HttpResponseNotAllowed, HttpResponseForbidden
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext, loader, Context
from YAASApp import form
from YAASApp.form import CreateUserForm, ChangeEmail, createAuction, BidForm
from YAASApp.models import Auction, Bid
from django.utils import translation
from django.core.mail import send_mail

# Create your views here.
def home(request):
    return render_to_response("home.html", {'form': form},context_instance= RequestContext(request))

def register(request):
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            new_user = User();
            new_user.username = form.cleaned_data['username']
            new_user.email = form.cleaned_data['email']
            new_user.set_password(form.cleaned_data['password'])
            new_user.save()
            return HttpResponseRedirect('/profile/')
    else:
        form = CreateUserForm(request.POST)
    return render_to_response("registration.html", {'form': form},context_instance= RequestContext(request))

def login_user(request):
    if request.method == 'POST':
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        nextTo = request.GET.get('next', '')            #retrieving the url to redirect after successful login

        user = auth.authenticate(username=username, password=password) #Authenticating the given user

        if user is not None:     #Check whether the user is authentication or not
            auth.login(request,user)    #Loging in the user

            if len(nextTo) != 0:
                return HttpResponseRedirect(nextTo)
            else:
                return HttpResponseRedirect('/profile/')
    else:
        error = "Please Sign in"
        return render_to_response("login.html", {'error': error},context_instance= RequestContext(request))
    return render_to_response("login.html", {},context_instance= RequestContext(request))

def all_auction(request):
    # try:
    #     if not request.session["lang"]:
    #         request.session["lang"] = "sv"
    #         translation.activate(request.session["lang"])
    #     else:
    #         translation.activate(request.session["lang"])
    # except KeyError:
    #     request.session["lang"] = "sv"
    #     translation.activate(request.session["lang"])
    auctions = Auction.objects.all()
    auctions = auctions.exclude(state='B')
    t = loader.get_template("archive.html")
    c = Context({'auctions' : auctions})
    return HttpResponse(t.render(c))

def post(request, id):
    auction = Auction.objects.get(id=id)
    bids = Bid.objects.filter(auction_id=id)
    t = loader.get_template("post.html")
    c = Context({'auction' : auction, 'bids':bids})
    return HttpResponse(t.render(c))

@login_required(login_url='/login/')
def user_profile(request):
    """ User profile page """
    user = User.objects.get(pk=request.user.pk)

    return render_to_response('user_profile.html', {
        'user': request.user,
        })

@login_required(login_url='/login/')
def change_email(request):
    # a common django idiom for forms
    user = User.objects.get(pk=request.user.pk)
    if request.method == 'POST':
        form = ChangeEmail(request.POST)
        if form.is_valid():
            if form.cleaned_data['email'] == form.cleaned_data['email_confirm']:
                user.email = form.cleaned_data['email']
                user.save()
                return HttpResponseRedirect('/profile/')
            else:
                form = ChangeEmail(request.POST)
    else:
        form = ChangeEmail(request.POST)
    return render_to_response('email.html', {'form': form},context_instance= RequestContext(request))


# @login_required
# def add_auction(request):
#     if not request.method == 'POST':
#         form = createAuction()
#         return render_to_response('createauction.html', {'form' : form}, context_instance=RequestContext(request))
#     else:
#         form = createAuction(request.POST)
#         if form.is_valid():
#             cd = form.cleaned_data
#             a_title = cd['title']
#             a_description = cd['description']
#             a_min_price = cd['min_price']
#             a_end_time = cd['end_time']
#             auction = Auction(seller = request.user, title =a_title, description = a_description, min_price = a_min_price, end_time = a_end_time, state = 'A')
#             auction.save()
#             return HttpResponseRedirect('/allauction/')
#         else:
#             form = createAuction()
#             return render_to_response('createauction.html', {'form' : form, "error" : "Not valid data" },  context_instance=RequestContext(request))

@login_required(login_url='/login/')
def add_auction(request):
    if not request.method == 'POST':
        form = createAuction()
        return render_to_response('createauction.html', {'form' : form}, context_instance=RequestContext(request))
    else:
        form = createAuction(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            a_title = cd['title']
            a_description = cd['description']
            a_min_price = cd['min_price']
            a_end_time = cd['end_time']
            #auction = Auction(seller = request.user, title =a_title, description = a_description, min_price = a_min_price, end_time = a_end_time, state = 'A')
            #auction.save()
            # form = createAuctionConf()
            return render_to_response("addAuctionConf.html",{'a_title':a_title, 'a_description':a_description, 'a_min_price':a_min_price, 'a_end_time':a_end_time},
                                      context_instance=RequestContext(request))
        else:
            form = createAuction()
            return render_to_response('createauction.html', {'form' : form, "error" : "Not valid data" },  context_instance=RequestContext(request))

def add_auctionConf(request):
    auction = Auction()
    answer = request.POST['answer']
    a_title = request.POST['a_title']
    a_description=request.POST['a_description']
    a_min_price=request.POST['a_min_price']
    endtime_raw= request.POST['a_end_time']
    endtime_str = str(endtime_raw)
    try:
        a_end_time = datetime.strptime(endtime_str, '%d-%m-%Y %H:%M')
    except ValueError:
        form = createAuction()
        return render_to_response('createauction.html',{'form' : form, "error" : "Not valid data" },
                                  context_instance=RequestContext(request))
    if answer == 'Yes':
        auction.title=a_title
        auction.description=a_description
        auction.min_price=a_min_price
        auction.end_time=a_end_time
        auction.seller_id=request.user.id
        auction.state='A'
        auction.save()
        send_mail('No-reply: Auction', 'Your auction has been created successfully', 'admin@example.com',
                  [request.user.email], fail_silently=False)
        return HttpResponseRedirect('/allauction/')
    else:
        return HttpResponseRedirect('/')

@login_required(login_url='/login/')
def edit_description(request, id):
    articles = Auction.objects.filter(id = id)
    if len(articles) > 0:
        article = Auction.getByID(id)
    else:
        article = Auction(id)

    if request.user.id == article.seller_id:
        if request.method=="POST" and request.POST.has_key('description'):
            article.description = request.POST["description"].strip()
            article.save()
            return HttpResponseRedirect('/allauction/'+id)
        else:
            return render_to_response("edit.html",
                                  {'id':article.id, 'description':article.description.strip()},
                                  context_instance=RequestContext(request))
    else:
        return HttpResponseRedirect('/allauction/')

@login_required(login_url='/login/')
def add_bid(request, id):
    auction = get_object_or_404(Auction, id = id)
    if auction.state == 'B':
        return HttpResponseRedirect('/allauction/'+id)
    if not request.method == 'POST':
        return render_to_response("bid.html", {'id':auction.id},
                                  context_instance=RequestContext(request))
    if not request.user.id == auction.seller_id:
        #print 'is not seller'
        form = BidForm(request.POST)
        new_bid_raw = request.POST['min_price']
        try:
            new_bid_dec = Decimal(new_bid_raw)
        except InvalidOperation:
            return render_to_response("bid.html", {'id':auction.id},
                                      context_instance=RequestContext(request))
        # if form.is_valid():
        #print 'is valid'
        bid_price = new_bid_dec
        highest_bid = auction.min_price
        prev_bidder = []
        if len(Bid.objects.filter(auction_id = id)) > 0:
            prev_bidder =  [Bid.objects.filter(auction_id = id).latest('id').bidder.email]
            highest_bid = Bid.objects.filter(auction_id = id).latest('id').bid_price

        if bid_price>highest_bid:
            print 'if condition'
            new_bid = Bid(bid_price = bid_price, auction_id= id, bidder_id = request.user.id)
            new_bid.save()
            send_mail('No-reply: Bid', 'Your bid has been added successfully', 'admin@example.com',
                      [request.user.email, auction.seller.email]+prev_bidder, fail_silently=False)
            return HttpResponseRedirect('/allauction/'+id)
        else:
            return render_to_response("bid.html", {'id':auction.id},
                                      context_instance=RequestContext(request))
        # highest_bid_amount = Bid.objects.filter(auction_id = id).aggregate(Max('bid_price')).get('amount__max')
        # if (bid_price > highest_bid_amount):
        #     print 'is high'
        #     new_bid = Bid(bid_price = bid_price, auction_id= id, bidder_id = request.user.id)
        #     new_bid.save()
        #     return HttpResponseRedirect('/allauction/')
        # else:
        #     print 'is not ok'
        #     return HttpResponseRedirect('/allauction/')

    # return render_to_response("bid.html", {'id':auction.id},
    #                               context_instance=RequestContext(request))
    else:
        return HttpResponseRedirect('/allauction/'+id)

def search(request):
    if request.method == 'POST':
        key_word = request.POST['search']
        auctions = Auction.objects.filter(title__contains = key_word)
        auctions = auctions.exclude(state = 'B')
        results = [auction for auction in auctions]
        return render_to_response('archive.html',{'auctions':results},context_instance=RequestContext(request))
    else:
        return render_to_response('search.html',context_instance=RequestContext(request))

def apisearch(request, title):
    auction = get_object_or_404(Auction, title=title)
    if not auction.state == 'B':
        try:
            json = serializers.serialize("json", [auction])
            response = HttpResponse(json, mimetype="application/json")
            response.status_code = 200
        except (ValueError, TypeError, IndexError):
            response = HttpResponse()
            response.status_code = 400
        return response
    else:
        response = HttpResponse()
        response.status_code = 400
        return response
# def switch_to_Swedish_link(request):


class APIBid:
    def __call__(self, request, username, auction_id):
        self.request = request
        # Look up the user and throw a 404 if it doesn't exist
        self.user = get_object_or_404(User, username=username)
        if not request.method in ["ADDBID"]:
            return HttpResponseNotAllowed(["ADDBID"])
            # Check and store HTTP basic authentication, even for methods that
        # don't require authorization.
        self.authenticate()
        # Call the request method handler
        if request.method=="ADDBID":
            return self.do_ADD()


    def authenticate(self):
        # Pull the auth info out of the Authorization: header
        auth_info = self.request.META.get("HTTP_AUTHORIZATION", None)
        #print self.request
        print auth_info
        if auth_info and auth_info.startswith("Basic "):
            basic_info = auth_info.split(" ", 1)[1]
            print basic_info, basic_info.decode("base64")
            u, p = basic_info.decode("base64").split(":")
            print u, p
            self.user = u
            # Authenticate against the User database. This will set
            # authenticated_user to None if authentication fails.
            self.authenticated_user = authenticate(username=u, password=p)
            print "self.authenticated_user,", self.authenticated_user
        else:
            self.authenticated_user = None

    def forbidden(self):
        response = HttpResponseForbidden()
        response["WWW-Authenticate"] = 'Basic realm="Auction"'
        return response

    def do_ADDBID(self):
        if self.user != str(self.authenticated_user):
            print "forbidden"
            return self.forbidden()
        else:
            print 'add bid'
            add_bid(request=self.request, id=self.auction_id)
            return

class force_lang:
    def __init__(self, new_lang):
        self.new_lang = new_lang
        self.old_lang = translation.get_language()
    def __enter__(self):
        translation.activate(self.new_lang)
    def __exit__(self, type, value, tb):
        translation.activate(self.old_lang)

#Vietnamese views
def home_vi(request):
    with force_lang('vi'):
        return render_to_response("home.html", {'form': form},context_instance= RequestContext(request))