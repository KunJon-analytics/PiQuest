$( document ).ready(
	function () {
		
		function marquee ( bar, speed, direction ) { //main marquee function
		
			//marquee text width
			var initWidth = $( bar + " .marquee-message" ).width();
			
			//initial position
			$( bar + " .marquee-message" ).css( 'margin-left', function () {
				return ( $( bar ).width() - initWidth ) / 2;
			} );
			
			if ( direction == 'left' ) { //from left to right
				//resetting the marquee element
				function resMarquee_left () {
					var left = -1 * initWidth;
					$( bar + " .marquee-message" ).css( 'margin-left', left );
				}
				
				//marquee function
				function marquee_left () {
					$( bar + " .marquee-message" ).css( 'margin-left', function ( index, val ) {
						return parseInt( val, 10 ) + speed + 'px';
					} );
					
					//reset the element if it's out of it's container
					if ( parseInt ( $( bar + " .marquee-message" ).css( 'margin-left' ) ) > $( bar ).width() ) {
						resMarquee_left ();
					}
				
				}
				
				setInterval( marquee_left, 10 );
			
			} else { //default: from right to left
				//marquee text width
				var initWidth = $( bar + " .marquee-message" ).width();
				
				//initial position
				$( bar + " .marquee-message" ).css( 'margin-left', function () {
					return ( $( bar ).width() - initWidth ) / 2;
				} );
			
				//resetting the marquee element
				function resMarquee_right () {
					$( bar + " .marquee-message" ).css( 'margin-left', $( bar ).width() );
				}
				
				//marquee function
				function marquee_right () {
					$( bar + " .marquee-message" ).css( 'margin-left', function ( index, val ) {
						return parseInt( val, 10 ) - speed + 'px';
					} );
					
					//reset the element if it's out of it's container
					if ( parseInt ( $( bar + " .marquee-message" ).css( 'margin-left' ) ) < -1 * $( bar + " .marquee-message" ).width() ) {
						resMarquee_right ();
					}
				
				}
				
				setInterval( marquee_right, 10 );
			
			}
		
			
			
		}
		
		
		marquee( ".marquee2", 1, 'right' );

	}
);