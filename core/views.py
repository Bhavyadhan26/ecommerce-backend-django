from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from django.contrib.auth import authenticate
from .models import Product, Cart, Order, OrderItem
from .serializers import ProductSerializer, CartSerializer, OrderSerializer, UserSerializer

@api_view(['POST'])
def signup(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({'message': 'User created successfully'}, status=201)
    return Response(serializer.errors, status=400)

@api_view(['POST'])
def login(request):
    username = request.data.get('username')
    password = request.data.get('password')
    user = authenticate(username=username, password=password)
    if user:
        return Response({'message': 'Login successful'})
    else:
        return Response({'error': 'Invalid credentials'}, status=400)

@api_view(['GET', 'POST'])
def products(request):
    if request.method == 'GET':
        items = Product.objects.all()
        serializer = ProductSerializer(items, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

@api_view(['POST'])
@authentication_classes([SessionAuthentication, BasicAuthentication])
@permission_classes([IsAuthenticated])
def add_to_cart(request):
    user = request.user
    product_id = request.data.get('product')
    quantity = int(request.data.get('quantity', 1))

    try:
        cart_item = Cart.objects.get(user=user, product_id=product_id)
        cart_item.quantity += quantity
        cart_item.save()
        return Response({'message': 'Quantity updated in cart'})
    except Cart.DoesNotExist:
        serializer = CartSerializer(data={
            'user': user.id,
            'product': product_id,
            'quantity': quantity
        })
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Item added to cart'}, status=201)
        return Response(serializer.errors, status=400)

@api_view(['GET'])
@authentication_classes([SessionAuthentication, BasicAuthentication])
@permission_classes([IsAuthenticated])
def view_cart(request):
    user = request.user
    cart_items = Cart.objects.filter(user=user)
    serializer = CartSerializer(cart_items, many=True)

    total = sum(item.product.price * item.quantity for item in cart_items)

    return Response({
        'cart_items': serializer.data,
        'total_price': total
    })

@api_view(['GET','POST'])
@authentication_classes([SessionAuthentication, BasicAuthentication])
@permission_classes([IsAuthenticated])
def checkout(request):
    user = request.user
    cart_items = Cart.objects.filter(user=user)

    if not cart_items.exists():
        return Response({'error': 'Cart is empty'}, status=400)

    order = Order.objects.create(user=user)

    for item in cart_items:
        OrderItem.objects.create(
            order=order,
            product=item.product,
            quantity=item.quantity,
            price=item.product.price  # snapshot price
        )

    cart_items.delete()

    return Response({'message': 'Order placed successfully'})

@api_view(['GET'])
@authentication_classes([SessionAuthentication, BasicAuthentication])
@permission_classes([IsAuthenticated])
def view_orders(request):
    user = request.user
    orders = Order.objects.filter(user=user).order_by('-created_at')
    serializer = OrderSerializer(orders, many=True)
    return Response(serializer.data)
